#
# Copyright (c) 2019 by cisco Systems, Inc.
# All rights reserved.
#
#
import threading
import itertools
from binascii import hexlify, unhexlify
from contextlib import contextmanager
import time
import grpc
from .sl_util import MplsUtil
from .sl_util import BatchUtil
from .sl_util import RouteUtil
from .sl_util import L2RouteUtil
from .grpc_client import GrpcClient
from genpy import sl_common_types_pb2
from genpy import sl_global_pb2
from util.util import LoggerStub as Logger

log = Logger(name="SLApiClient")


class SLApiBase:
    def __init__(self, host, port, do_global_init,  init_params):
        """
        Initialize connection and start global thread

        :param client: Primary Grpc client to be used
        :type client: SLGrpcClient

        :param global_notif_client: Grpc client to be used by global notif thread
        :type client: SLGrpcClient

        :param json_params: json test param dictionary
        :type client: dict
        """
        self._host = host
        self._port = port
        self.do_global_init = do_global_init
        self.client = GrpcClient(self._host, self._port)
        if do_global_init:
            self.global_notif_client = GrpcClient(self._host, self._port)
            self.global_notif_thread = None

            self._start_global_notif_thread(init_params)

    def _start_global_notif_thread(self, init_params):
        """Start global notif thread and wait for global init response"""
        event = threading.Event()

        self.global_notif_thread  = threading.Thread(target=self.global_init,
                             args=(event, init_params))
        self.global_notif_thread.start()

        # Wait to hear from the server - Thread is blocked
        log.info("Waiting to hear from Global thread...")
        event.wait()
        log.info("Global Event Notification Received! Waiting for events...")

    # Wait on Global notification events
    def global_init(self, event, init_params):
        retry_count = 6

        for i in range(1, retry_count):
            try:
                self.global_notifs = self.global_notif_client.global_init(init_params)
                response = next(self.global_notifs)
                if response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_ERROR:
                    if (response.ErrStatus.Status ==
                            sl_common_types_pb2.SLErrorStatus.SL_NOTIF_TERM):
                            log.info("SL takenover by anothet Global Init RPC. NOT EXPECTED")
                    else:
                        # If this session is lost, then most likely the server restarted
                        log.error("global_init: exiting unexpectedly, Server Restart?")
                        log.error("last response from server: %s" % response)
                    # Retry on error
                    continue

                err_status = sl_common_types_pb2.SLErrorStatus
                if response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_VERSION:
                    if response.ErrStatus.Status in { err_status.SL_SUCCESS,
                                                      err_status.SL_INIT_STATE_CLEAR,
                                                      err_status.SL_INIT_STATE_READY }:

                        log.info("Server Returned 0x%x, Server's Version %d.%d.%d" % (
                            response.ErrStatus.Status,
                            response.InitRspMsg.MajorVer,
                            response.InitRspMsg.MinorVer,
                            response.InitRspMsg.SubVer))

                        # Successfully Initialized
                        # Notify the main thread to proceed
                        event.set()
                    else:
                        log.info("Init failed with status %s" % 
                                response.ErrStatus.Status)
                        continue

                self._global_notif_handler()

            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.UNAVAILABLE:
                    # One less than retry count so that we can dump exception
                    # if grpc server cannot be reached
                    if i < retry_count - 1:
                       log.info("Retry {} of global init as server not available"
                             .format(i))
                       time.sleep(30)
                       continue

                # Main thread will close this channel on cleanup
                if e.code() == grpc.StatusCode.CANCELLED:
                    log.info("Stream canceled. Exiting...")
                    return

                log.error("Received exception:", e)
                log.error("Server died?")


    def _global_notif_handler(self):
        """
        Global notification handler
        Iterate over stream of global notifications
        """
        err_status = sl_common_types_pb2.SLErrorStatus
        for response in self.global_notifs:
            if response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_HEARTBEAT:
                log.info("Received Event: Heartbeat")
            elif response.EventType == sl_global_pb2.SL_GLOBAL_EVENT_TYPE_ERROR:
                if response.ErrStatus.Status in {
                    err_status.SL_VRF_V4_ROUTE_REPLAY_FATAL_ERROR,
                    err_status.SL_VRF_V6_ROUTE_REPLAY_FATAL_ERROR,
                    err_status.SL_VRF_V4_ROUTE_REPLAY_OK,
                    err_status.SL_VRF_V6_ROUTE_REPLAY_OK }:

                    log.error("Received Route FATAL Global Error event: %s" % response)
                elif response.ErrStatus.Status in {
                      err_status.SL_ILM_REPLAY_FATAL_ERROR,
                      err_status.SL_ILM_REPLAY_OK }:

                    log.error("Received MPLS FATAL Global Error event: %s" % response)

                log.info("Received Global Error event: %s" % response)
                return
            else:
                log.error("Received unknown event: %s" % response)
                return


    def cleanup(self):
        # Cancel global notif stream
        if self.do_global_init:
            self.global_notifs.cancel()

        try:
            # Earlier grpc version do not support this
            self.client.channel.close()
            if self.do_global_init:
                self.global_notif_client.channel.close()
        except AttributeError:
            pass
        if do_global_init:
            self.global_notif_thread.join()

    @contextmanager
    def notif_channel(self):
        """Start global notif thread and wait for global init response"""
        client = GrpcClient(self._host, self._port)
        try:
            yield client
        finally:
            try:
                # Earlier grpc version do not support this
                client.channel.close()
            except AttributeError:
                pass

    def _stream_and_validate(self, op, validator, *args, xcount=None, xfail=False, **kwargs):
        responses = op(*args, **kwargs)
        count = itertools.count()
        for response, _ in zip(responses, count):
            assert xfail ^ validator(response)
        
        if xcount:
            assert next(count) == next(xcount)

    def _send_and_validate(self, op, validator, *args, xfail=False, **kwargs):
        response = op(*args, **kwargs)

        assert xfail ^ validator(response)

        return response

    def _crud_op_stream(self, op_info, retriever, af, *args, paths=None, next_hops=None, **kwargs):
        key, iterable = retriever(op_info, af, paths)
        batch_kwargs = {
                'iterable': iterable,
                'size': op_info.get('batch_size', 1),
                'af': af,
                'paths': paths,
                'next_hops': next_hops,
                'correlator': op_info.get('correlator', 0)
                }

        batch_info = dict(op_info) # work on a copy

        count = itertools.count()
        def iterator():
            # Zip with count to keep track of number of batches generated
            for batch, _ in zip(BatchUtil.gen_batches(**batch_kwargs), count):
                batch_info[key] = batch 
                yield batch_info

        stream_info = {'af': af, 'iterator': iterator()}
        self._stream_and_validate(*args, stream_info, xcount=count, **kwargs)

    def _crud_op(self, op_info,  retriever, af, *args, paths=None, next_hops=None, **kwargs):
        key, iterable = retriever(op_info, af, paths)
        batch_kwargs = {
                'iterable': iterable,
                'size': op_info.get('batch_size', 1),
                'af': af,
                'paths': paths,
                'next_hops': next_hops,
                'correlator': op_info.get('correlator', 0)
                }

        batch_info = dict(op_info) # work on a copy

        for batch in BatchUtil.gen_batches(**batch_kwargs):
            batch_info[key] = batch 
            self._send_and_validate(*args, batch_info, **kwargs)

    def _get_op(self, get_info, grpc_op, validator, *args, af=None, **kwargs):
        if af:
            get_info['af'] = af

        return self._send_and_validate(grpc_op, validator, get_info, *args, **kwargs)
        
    def _get_op_iterator(self, iterator, op, validator, *args, af=None, xfail=False, **kwargs):
        stream_info = {'iterator': iterator}
        if af:
            stream_info['af'] = af

        responses = op(stream_info, *args, **kwargs)
        for response in responses:
            assert xfail ^ validator(response)
            yield response

    def _get_all(self, op, get_info, retriever, xfail=False, xcount=None, **kwargs):
        _get_info = dict(get_info) # operate on a copy

        def gen_get_info():
            yield _get_info
            _get_info['get_next'] = 1
            while response.Entries and not response.Eof:
                for key, obj in retriever(response):
                    _get_info[key] = obj
                    yield _get_info

        responses = []
        for info in gen_get_info():
            response = op(info, xfail=xfail, **kwargs)
            responses.extend(response.Entries)

        if xcount:
            assert len(responses) == xcount

        return responses


class SLApiClient(SLApiBase):
    "Represents a SL API session"

    def __init__(self, client, global_notif_client, do_global_init, json_params):
        super(SLApiClient, self).__init__(client, 
                global_notif_client, do_global_init, json_params)

    ###### Route Vertical ######

    def route_global_get(self, af):
        self._send_and_validate(self.client.route_global_get,
                                RouteUtil.print_route_globals,
                                af=af)

    def route_global_stats_get(self, af):
        self._send_and_validate(self.client.route_global_stats_get,
                                RouteUtil.print_route_stats_globals,
                                af)

    def vrf_register(self, vrf_params):
        self._send_and_validate(self.client.vrf_registration_add,
                                RouteUtil.validate_vrf_response,
                                vrf_params)

    def vrf_registration_eof(self, vrf_params):
        self._send_and_validate(self.client.vrf_registration_eof,
                                RouteUtil.validate_vrf_response,
                                vrf_params)

    def vrf_unregister(self, vrf_params):
        self._send_and_validate(self.client.vrf_registration_delete,
                                RouteUtil.validate_vrf_response,
                                vrf_params)

    def vrf_get(self, get_info, af, stats=False, xfail=False):
        '''
        Streaming not supported for label block operations
        '''
        op, grpc_op = self._get_op, self.client.vrf_get 
        if stats:
            validator = RouteUtil.validate_vrf_get_response
        else:
            validator = RouteUtil.validate_vrf_stats_get_response

        return op(get_info, grpc_op, validator, stats, af=af, xfail=xfail)

    def vrf_get_all(self, get_info, af, stats=False, xfail=False):
        '''
        Streaming not supported for label block operations
        '''
        op, grpc_op = self._get_all, self.vrf_get
        retriever = RouteUtil.get_last_vrf

        return op(grpc_op, get_info, retriever, af=af, stats=stats, xfail=xfail)

    def route_add(self, route_info, af, stream=False, xfail=False, paths=None, next_hops=None):
        if stream:
            op, grpc_op = self._crud_op_stream, self.client.route_add_stream
        else:
            op, grpc_op = self._crud_op, self.client.route_add

        retriever = RouteUtil.retrieve_routes
        validator = RouteUtil.validate_route_response

        op(route_info, retriever, af, grpc_op, validator, xfail=xfail, paths=paths, next_hops=next_hops)

    def route_update(self, route_info, af, stream=False, xfail=False, paths=None, next_hops=None):
        if stream:
            op, grpc_op = self._crud_op_stream, self.client.route_update_stream
        else:
            op, grpc_op = self._crud_op, self.client.route_update
        retriever = RouteUtil.retrieve_routes

        validator = RouteUtil.validate_route_response

        op(route_info, retriever, af, grpc_op, validator, xfail=xfail, paths=paths, next_hops=next_hops)

    def route_delete(self, route_info, af, stream=False, xfail=False, paths=None, next_hops=None):
        if stream:
            op, grpc_op = self._crud_op_stream, self.client.route_delete_stream
        else:
            op, grpc_op = self._crud_op, self.client.route_delete

        retriever = RouteUtil.retrieve_routes
        validator = RouteUtil.validate_route_response

        op(route_info, retriever, af, grpc_op, validator, xfail=xfail, paths=paths, next_hops=next_hops)

    def route_get(self, get_info, af, stream=False, xfail=False):
        if stream:
            op, grpc_op = self._get_op_iterator, self.client.route_get_stream
        else:
            op, grpc_op = self._get_op, self.client.route_get

        validator = RouteUtil.validate_route_get_response

        return op(get_info, grpc_op, validator, af=af, xfail=xfail)

    def route_get_all(self, get_info, af, xfail=False):
        '''
        This operation does not support streaming as each request after the
        first is dependant on the previous response.
        '''
        op, grpc_op = self._get_all, self.route_get 

        if af == 4:
            retriever = RouteUtil.get_last_prefix_v4
        else:
            retriever = RouteUtil.get_last_prefix_v6

        return op(grpc_op, get_info, retriever, af=af, xfail=xfail)

    
    ###### Mpls Vertical ######

    def mpls_global_get(self, **kwargs):
        self._send_and_validate(self.client.mpls_global_get,
                                MplsUtil.validate_mpls_globals)

    def mpls_register(self, reg_params):
        self._send_and_validate(self.client.mpls_register_oper,
                                MplsUtil.validate_mpls_regop_response,
                                reg_params)

    def mpls_eof(self):
        self._send_and_validate(self.client.mpls_eof_oper,
                                MplsUtil.validate_mpls_regop_response)

    def mpls_unregister(self):
        self._send_and_validate(self.client.mpls_unregister_oper,
                                MplsUtil.validate_mpls_regop_response)

    def label_block_add(self, block_params, **kwargs):
        self._send_and_validate(self.client.label_block_add,
                                MplsUtil.validate_lbl_blk_response,
                                block_params, **kwargs)

    def label_block_delete(self, block_params, **kwargs):
        self._send_and_validate(self.client.label_block_delete,
                                MplsUtil.validate_lbl_blk_response,
                                block_params, **kwargs)

    def label_block_get(self, get_info, xfail=False):
        '''
        Streaming not supported for label block operations
        '''
        op, grpc_op = self._get_op, self.client.label_block_get 
        validator = MplsUtil.validate_ilm_get_response

        return op(get_info, grpc_op, validator, xfail=xfail)

    def label_block_get_all(self, get_info, xfail=False):
        '''
        Streaming not supported for label block operations
        '''
        op, grpc_op = self._get_all, self.label_block_get
        retriever = MplsUtil.get_last_label_block

        return op(grpc_op, get_info, retriever, xfail=xfail)

    def ilm_add(self, ilm_info, af, stream=False, xfail=False, paths=None, next_hops=None):
        if stream:
            op, grpc_op = self._crud_op_stream, self.client.ilm_add_stream
        else:
            op, grpc_op = self._crud_op, self.client.ilm_add

        retriever = MplsUtil.retrieve_ilms
        validator = MplsUtil.validate_ilm_response

        op(ilm_info, retriever, af, grpc_op, validator, xfail=xfail, paths=paths, next_hops=next_hops)

    def ilm_update(self, ilm_info, af, stream=False, xfail=False, paths=None, next_hops=None):
        if stream:
            op, grpc_op = self._crud_op_stream, self.client.ilm_update_stream
        else:
            op, grpc_op = self._crud_op, self.client.ilm_update
        retriever = MplsUtil.retrieve_ilms

        validator = MplsUtil.validate_ilm_response

        op(ilm_info, retriever, af, grpc_op, validator, xfail=xfail, paths=paths, next_hops=next_hops)

    def ilm_delete(self, ilm_info, af, stream=False, xfail=False, paths=None, next_hops=None):
        if stream:
            op, grpc_op = self._crud_op_stream, self.client.ilm_delete_stream
        else:
            op, grpc_op = self._crud_op, self.client.ilm_delete

        retriever = MplsUtil.retrieve_ilms
        validator = MplsUtil.validate_ilm_response

        op(ilm_info, retriever, af, grpc_op, validator, xfail=xfail, paths=paths, next_hops=next_hops)

    def ilm_get(self, get_info, stream=False, xfail=False):
        if stream:
            op, grpc_op = self._get_op_iterator, self.client.ilm_get_stream
        else:
            op, grpc_op = self._get_op, self.client.ilm_get

        validator = MplsUtil.validate_ilm_get_response

        return op(get_info, grpc_op, validator, xfail=xfail)

    def ilm_get_all(self, get_info, xfail=False, xcount=None):
        '''
        This operation does not support streaming as each request after the
        first is dependant on the previous response.
        '''
        op, grpc_op = self._get_all, self.ilm_get 
        retriever = MplsUtil.get_last_ilm 

        return op(grpc_op, get_info, retriever, xfail=xfail, xcount=xcount)

    #### L2 Vertical ###

    def l2_route_op_stream(self, *args, **kwargs):
        '''
        This operation doesn't support batching (retrievers) at the moment
        '''
        op, grpc_op = self._stream_and_validate, self.client.l2_route_op_stream
        validator = L2RouteUtil.validate_l2route_response

        return op(grpc_op, validator, *args, **kwargs)
