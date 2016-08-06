### Service Layer API

In IOS-XR, routing protocols make use of services provided by the Routing Information Base (RIB), the MPLS label manager, BFD, and other modules, in order to program the forwarding plane. Such programming is exposed through the service layer API, which is very rich in nature.

Exposing the service layer API as a Google RPC (or GRPC), over Google protocol buffers (protobuf or GPB), enables customers to write their own applications, routing protocols, controllers, etc., whether on box or off box, in a rich set of languages including cplusplus, python, GO, etc.

The Service Layer API is currently organized in a set of files that expose certain verticals e.g. IPv4 RIB functionality, or MPLS functionality, etc.
In the initial release, the focus is to provide the following verticals:

* Initialization: This mainly handles global initialization, and sets up an event notification channel based on GRPC streaming mechanism.
* IPv4, IPv6 Route: This mainly handles any IPv4 or IPv6 route additions into the node based on a certain VRF.
* MPLS Incoming Label Maps (ILMs): This mainly handles any incoming MPLS label mapping to a forwarding function.
* IPv4, IPv6 BFD: This mainly handles managing BFD sessions, and getting corresponding BFD session state notifications.
* Interfaces: This mainly allows registered clients to get interface state event notifications.
* More functions may be added in the future.

Each function vertical, e.g. RIB vertical, declares a "template" set of RPCs that is more or less consistently followed throughout other verticals. Some of these template RPCs are explained here:

* **(Vertical)Get()**: This is mainly used to query certain capabilities for that vertical.
* **(Vertical)GetStats()**: This is mainly used to query vertical specific statistics.
* **(Vertical)RegOp()**: This is mainly used to Register/Unregister/EoF, which basically notifies the service layer server about interest in the vertical, no interest, and end of file (EoF), respectively. The EoF marker is especially useful on replay of objects in certain restart scenarios.
* **(Vertical)(Object)Op()**: This is mainly used to add, delete, update objects. The convention used for add and update, is that, object 'adds' may fail if the object already exists, whereas update can create or simply override the object if it exists.
* **(Vertical)(Object)Get()**: This is mainly used to retrieve an object or a set of objects.
* **Stream()**: This is mainly a GRPC "streaming" version of the non-streaming version of the function.
* **Notif()**: This is mainly a streaming notification function, e.g. asynchronous BFD session state events' streaming.

The Service Layer API allows for GRPC unary functions in most cases, and GRPC streaming in other cases. The former can be rendered in both synchronous and asynchronous modes (depends on the language). The latter is used for continuous transmitting and/or receiving of objects in an asynchronous fashion. This is especially useful to boost performance in certain cases. Please refer to the GRPC website for more information: <http://grpc.io>
In addition, certain RPCs may also allow for batching e.g. creating a number of routes in a single RPC call (in a batch).

Each RPC usually takes a GRPC "message" or request, typically labeled (Something)Msg, example SLRoutev4Msg, which defines the parameters of the request, and return another "message", typically labeled (Something)MsgRsp as a response to the RPC request, example SLRoutev4MsgRsp.

Note that all files are annotated with detailed documentation.
The user of the API can use doxygen to render his/her own local documentation, refer to instructions under docs directory. The html generated documentation is broken up into sections that describe the messages, verticals, files, etc, and are very useful for quick reference.

Finally, please note that the API comes with:

* A quick start tutorial written in pyhton. The intent here is to get the user a jump-start on hooking up with the API. The reader is advized to try this next.

```
This can be found here: grpc/python/src/tutorial/
```

* Another similar tutorial written in GO (golang). This tutorial's code is pre-compiled and committed in the code repo for a quick start on some of the API key features showing batching, etc.

```
This can be found here: grpc/go/src/tutorial/quickstart.go
The executable can be found here: grpc/go/src/tutorial/tutorial
```

* A Python unittest regression suite that covers basic API sanities. It is also very useful and handy if someone wants to get some reference implementation for a certain use case.

```
This can be found here: grpc/python/src
```

To run the unit test regression, setup some Environment variables:

```
export SERVER_IP=192.168.122.192
export SERVER_PORT=57344
```

Run All tests:

```
python -m unittest -v tests.test_lindt
```

We hope that the above was useful quick overview about the service layer API. We recommend that the reader goes over the python quick tutorial first and then go over the .proto files under grpc/protos (or look at the generated .html pages, these are not kept in this repo, but can be auto-generated from this repo).
