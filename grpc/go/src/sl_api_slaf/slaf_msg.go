/*
 * Copyright (c) 2025 by cisco Systems, Inc.
 * All rights reserved.
 */
package sl_api_slaf

import (
    "fmt"
    "math/big"
    "net"
    "io"
    "encoding/binary"
    "strings"
    "time"

    log "github.com/sirupsen/logrus"
    pb "gengo"
    "golang.org/x/net/context"
    "google.golang.org/grpc"
    "google.golang.org/grpc/metadata"
)

var ClientID string = "521";
var GlobalOperationID uint64 = 0

var (
    MaxIlmInBatch uint32
    MaxBatchSize uint32
)

/*
 * Given an interface name, e.g, GigabitEthernet0/0/0/x, increment
 * x given the index (idx) and the maxIfIdx which should be the maximum
 * value of x
 *
 * Return the input string unchanged if:
 *   a) There is no "/" in the string
 *   b) idx or maxIfIdx are 0
 */

 func ifMunge(ifName string, idx uint, maxIfIdx uint) string {
    if maxIfIdx == 0 || idx == 0 {
        return ifName
    }
    i := strings.LastIndex(ifName, "/")
    if i > -1 {
        ifLeft := ifName[:i]
        ifIdx := ifName[i+1]
        return ifLeft + "/" + string(uint(ifIdx) + (idx % maxIfIdx))
    }
    return ifName
}

func incrementIpv4Pfx(pfx uint32, prefixLen uint32) (uint32){
    if prefixLen > 32 {
        log.Fatalf("PrefixLen > 32")
    }

    return (pfx + 1<<(32-prefixLen))
}

func ip4toInt(IPv4Address net.IP) uint32 {
    IPv4Int := big.NewInt(0)
    IPv4Int.SetBytes(IPv4Address.To4())
    return uint32(IPv4Int.Int64())
}

func int2ip4(IPv4Address uint32) net.IP {
        ip := make(net.IP, 4)
        binary.BigEndian.PutUint32(ip, IPv4Address)
        return ip
}

/* Start of Client Initialization functions */
func ClientInit(conn *grpc.ClientConn, username string, password string) (int) {
    /* Setup a go-routine channel to synchronize both go-routines*/
    sync_chan := make(chan int)

    /* Setup the notification channel */
    go setupNotifChannel(conn, sync_chan, username, password)

    /* Wait for response 0: error. 1: all ok*/
    wait_resp := <- sync_chan
    if wait_resp == 0 {
        fmt.Println("Client Error")
        return 0
    }

    /* Create a sLGlobalClient instance */
    globalClient := pb.NewSLGlobalClient(conn)

    /* Create a SLGlobalsGetMsg */
    globalGetMsg := &pb.SLGlobalsGetMsg {}

    /* new context with metadata */
    ctx := metadata.AppendToOutgoingContext(context.Background(),
        "username", username, "password", password)

    /* RPC to Get the globals. */
    response, err := globalClient.SLGlobalsGet(ctx,
        globalGetMsg)
    if err != nil {
        fmt.Println("Client Error %v", err)
        return 0
    }

    /* Print Server response */
    fmt.Println("MaxVrfNameLength: ", response.GetMaxVrfNameLength())
    fmt.Println("MaxInterfaceNameLength: ", response.GetMaxAFOpsPerMsg())
    fmt.Println("MaxPathsPerEntry:", response.GetMaxPathsPerEntry())
    fmt.Println("MaxPrimaryPathPerEntry: ", response.GetMaxPrimaryPathPerEntry())
    fmt.Println("MaxBackupPathPerEntry: ", response.GetMaxBackupPathPerEntry())
    fmt.Println("MaxMplsLabelsPerPath: ", response.GetMaxMplsLabelsPerPath())
    fmt.Println("MinPrimaryPathIdNum: ", response.GetMinPrimaryPathIdNum())
    fmt.Println("MaxPrimaryPathIdNum: ", response.GetMaxPrimaryPathIdNum())
    fmt.Println("MinBackupPathIdNum: ", response.GetMinBackupPathIdNum())
    fmt.Println("MaxBackupPathIdNum: ", response.GetMaxBackupPathIdNum())
    fmt.Println("MaxRemoteAddressNum: ", response.GetMaxRemoteAddressNum())
    fmt.Println("MaxL2BdNameLength: ", response.GetMaxL2BdNameLength())
    fmt.Println("MaxL2PmsiTunnelIdLength: ", response.GetMaxL2PmsiTunnelIdLength())
    fmt.Println("MaxLabelBlockClientNameLength: ", response.GetMaxLabelBlockClientNameLength())
    fmt.Println("MaxPathsInNexthopNotif: ", response.GetMaxPathsInNexthopNotif())
    fmt.Println("MaxVrfRegPerMsg: ", response.GetMaxVrfRegPerMsg())
    fmt.Println("MaxAFOpsPerMsg: ", response.GetMaxAFOpsPerMsg())
    fmt.Println("MaxNotifReqPerSLAFNotifReq: ", response.GetMaxNotifReqPerSLAFNotifReq())
    fmt.Println("MaxMatchFilterInBgplsTopoNotif: ", response.GetMaxMatchFilterInBgplsTopoNotif())

    MaxIlmInBatch = response.GetMaxAFOpsPerMsg()
    MaxBatchSize = response.GetMaxAFOpsPerMsg()

    return wait_resp
}

func setupNotifChannel(conn *grpc.ClientConn, sync_chan chan int,
                       username string, password string) {
    /* Create a sLGlobalClient instance */
    globalClient := pb.NewSLGlobalClient(conn)

    /* Create a SLGlobalsGetMsg */
    initMsg := &pb.SLInitMsg {
        MajorVer: uint32(pb.SLVersion_SL_MAJOR_VERSION),
        MinorVer: uint32(pb.SLVersion_SL_MINOR_VERSION),
        SubVer: uint32(pb.SLVersion_SL_SUB_VERSION),
    }

    /* context with metadata */
    ctx := metadata.AppendToOutgoingContext(context.Background(),
        "username", username, "password", password)

    /* RPC to Init the notification channel */
    stream, err := globalClient.SLGlobalInitNotif(ctx,
        initMsg)
    if err != nil {
        fmt.Println("Client Error %v", err)
        /*signal error*/
        sync_chan <- 0
        return
    }

    /* For ever read from stream */
    for {
        event, stream_err := stream.Recv()
        if stream_err != nil {
            fmt.Println("Client Recv Error %v", stream_err)
            break
        }

        switch event.EventType {
        case pb.SLGlobalNotifType_SL_GLOBAL_EVENT_TYPE_VERSION:
            initMsgRsp := event.GetInitRspMsg()
            /* Check Server event */
            if (event.ErrStatus.Status == pb.SLErrorStatus_SL_SUCCESS) ||
               (event.ErrStatus.Status ==
                   pb.SLErrorStatus_SL_INIT_STATE_CLEAR) ||
               (event.ErrStatus.Status ==
                   pb.SLErrorStatus_SL_INIT_STATE_READY) {
                fmt.Printf("Server Returned %s, Version: %d.%d.%d\n",
                    event.ErrStatus.Status.String(),
                    initMsgRsp.MajorVer, initMsgRsp.MinorVer, initMsgRsp.SubVer)
                /*signal success, continue processing events from server*/
                sync_chan <- 1
            } else {
                log.Fatalf("Client Recv Error 0x%x", event.ErrStatus.Status)
            }

        case pb.SLGlobalNotifType_SL_GLOBAL_EVENT_TYPE_ERROR:
            if (event.ErrStatus.Status == pb.SLErrorStatus_SL_NOTIF_TERM) {
                log.Fatalf("Received notice to terminate. Client Takeover?\n")
            }
            log.Fatalf("Error not handled: 0x%x", event.ErrStatus.Status)

        case pb.SLGlobalNotifType_SL_GLOBAL_EVENT_TYPE_HEARTBEAT:
            fmt.Printf("Received HeartBeat\n")

        default:
            log.Fatalf("Client Recv unknown event %s",
                event.EventType.String())
        }
    }

    log.Fatalf("Exiting")
}
/* End of Client Initialization functions */

/* V2SLAF VRF Registration function */
func SlafVrfRegOperation(conn *grpc.ClientConn, oper pb.SLRegOp,
    tableType pb.SLTableType,
    username string, password string) {

    /* Create a NewSLAFClient instance */
    client := pb.NewSLAFClient(conn)
    /* Create an Vrf Reg registration message */
    vrf_reg_msg := []*pb.SLAFVrfReg{
        &pb.SLAFVrfReg{
            Table: tableType,
            VrfReg: &pb.SLVrfReg{
                VrfName: "default",
                AdminDistance: uint32(99),
                VrfPurgeIntervalSeconds: uint32(500),
            },
        },
    }
    message := &pb.SLAFVrfRegMsg{
                    Oper: oper,
                    VrfRegMsgs: vrf_reg_msg,
                }

    ctx := metadata.AppendToOutgoingContext(context.Background(),
                    "username", username, "password", password,
                    "iosxr-slapi-clientid", ClientID)

    /* Call the SLAF Vrf Register rpc */
    response, err := client.SLAFVrfRegOp(ctx, message)
    if err != nil {
        log.Fatal(err)
    }

    if response.StatusSummary.Status != pb.SLErrorStatus_SL_SUCCESS {
        log.Fatalf("Registration operation error: ", response.String())
    }

    log.Info("Response: ", response)
}

/* Performs the SLAFOp Unary rpc */
func runSlafOpRequest(conn *grpc.ClientConn, messages []*pb.SLAFMsg,
                      tableType pb.SLTableType, username string, password string) (err error) {

    client := pb.NewSLAFClient(conn)
    ctx, cancel := context.WithTimeout(context.Background(), 600*time.Second)
    ctx = metadata.AppendToOutgoingContext(ctx,
        "username", username, "password", password,
        "iosxr-slapi-clientid", ClientID)
    defer cancel() // make sure all paths cancel the context to avoid context leak

    for _, message := range messages {
        /* Unary RPC to program routes. */
        response, err := client.SLAFOp(ctx, message)
        if err != nil {
            return err
        }

        results := response.GetResults()
        for i := 0; i < len(results); i++ {
            if results[i].GetStatus().GetStatus() != pb.SLErrorStatus_SL_SUCCESS {
                if tableType == pb.SLTableType(pb.SLTableType_SL_IPv4_ROUTE_TABLE) {
                    err = fmt.Errorf("route operation failed for: %s/%d ErrorStatus: %s With OperationID: %d",
                                results[i].GetKey().GetIPRoutePrefix().GetPrefix(),
                                results[i].GetKey().GetIPRoutePrefix().GetPrefixLen(),
                                results[i].GetStatus().GetStatus(),
                                results[i].GetOperationID())
                }
                if tableType == pb.SLTableType(pb.SLTableType_SL_MPLS_LABEL_TABLE) {
                    err = fmt.Errorf("route operation failed for: %s ErrorStatus: %s With OperationID: %d",
                                results[i].GetKey().GetMplsLabel(),
                                results[i].GetStatus().GetStatus(),
                                results[i].GetOperationID())
                }
                if tableType == pb.SLTableType(pb.SLTableType_SL_PATH_GROUP_TABLE) {
                    err = fmt.Errorf("route operation failed for: %s FibErrorStatus: %s With OperationID: %d",
                                results[i].GetKey().GetPathGroupId(),
                                results[i].GetStatus().GetStatus(),
                                results[i].GetOperationID())
                }
            } else {
                log.Info("Response: ", results[i])
            }
        }
    }
    return err;
}

/* Performs the SLAFOpStream rpc */
func runSlafOpStreamRequest(conn *grpc.ClientConn, messages []*pb.SLAFMsg,
                            totalOperations uint, fibCheck bool,
                            tableType pb.SLTableType, username string, password string) (err error) {

        client := pb.NewSLAFClient(conn)
        ctx, cancel := context.WithTimeout(context.Background(), 600*time.Second)
        ctx = metadata.AppendToOutgoingContext(ctx,
            "username", username, "password", password,
            "iosxr-slapi-clientid", ClientID)
        defer cancel() // make sure all paths cancel the context to avoid context leak

        stream, err := client.SLAFOpStream(ctx)
        if err != nil {
                return err
        }

        /* Use the expected number of routes to close the errc channel*/
        numOperations := totalOperations
        errc := make(chan error, 1)

        go func() {
                for {
                    if numOperations == 0 {
                        /* Stream will never return an EOF so use number of routes to indicate when stream should finish */
                        close(errc)
                        return
                    }
                    response, errMsg := stream.Recv()
                    log.Info("stream: ", response, errMsg)
                    if errMsg == io.EOF {
                            // read done.
                            close(errc)
                            return
                    }
                    if errMsg != nil {
                            log.Error(errMsg)
                            errc <- errMsg
                            close(errc)
                            return
                    }
                    results := response.GetResults()
                    for i := 0; i < len(results); i++ {
                        if results[i].GetStatus().GetStatus() != pb.SLErrorStatus_SL_SUCCESS {
                            if tableType == pb.SLTableType(pb.SLTableType_SL_IPv4_ROUTE_TABLE) {
                                errc <- fmt.Errorf("route operation failed for: %s/%d ErrorStatus: %s With OperationID: %d",
                                                results[i].GetKey().GetIPRoutePrefix().GetPrefix(),
                                                results[i].GetKey().GetIPRoutePrefix().GetPrefixLen(),
                                                results[i].GetStatus().GetStatus(),
                                                results[i].GetOperationID())
                            }

                            if tableType == pb.SLTableType(pb.SLTableType_SL_MPLS_LABEL_TABLE) {
                                errc <- fmt.Errorf("route operation failed for: %s ErrorStatus: %s With OperationID: %d",
                                                results[i].GetKey().GetMplsLabel(),
                                                results[i].GetStatus().GetStatus(),
                                                results[i].GetOperationID())
                            }
                            if tableType == pb.SLTableType(pb.SLTableType_SL_PATH_GROUP_TABLE) {
                                errc <- fmt.Errorf("route operation failed for: %s FibErrorStatus: %s With OperationID: %d",
                                                results[i].GetKey().GetPathGroupId(),
                                                results[i].GetStatus().GetStatus(),
                                                results[i].GetOperationID())
                            }
                        } else {
                            /* We expect only a Rib Ack */
                            if fibCheck == false {
                                log.Info("Response: ", results[i])
                            }
                        }
                        if fibCheck {
                            /* Fib status of Unknown indicates the current response did not contain a fib response */
                            if results[i].GetFIBStatus() != pb.SLAFFibStatus_SL_FIB_UNKNOWN {
                                numOperations--
                                if results[i].GetFIBStatus() != pb.SLAFFibStatus_SL_FIB_SUCCESS {
                                    if tableType == pb.SLTableType(pb.SLTableType_SL_IPv4_ROUTE_TABLE) {
                                        errc <- fmt.Errorf("route operation failed for: %s/%d FibErrorStatus: %s With OperationID: %d",
                                                        results[i].GetKey().GetIPRoutePrefix().GetPrefix(),
                                                        results[i].GetKey().GetIPRoutePrefix().GetPrefixLen(),
                                                        results[i].GetFIBStatus(),
                                                        results[i].GetOperationID())
                                    }
                                    if tableType == pb.SLTableType(pb.SLTableType_SL_MPLS_LABEL_TABLE) {
                                        errc <- fmt.Errorf("route operation failed for: %s FibErrorStatus: %s With OperationID: %d",
                                                        results[i].GetKey().GetMplsLabel(),
                                                        results[i].GetFIBStatus(),
                                                        results[i].GetOperationID())
                                    }
                                    if tableType == pb.SLTableType(pb.SLTableType_SL_PATH_GROUP_TABLE) {
                                        errc <- fmt.Errorf("route operation failed for: %s FibErrorStatus: %s With OperationID: %d",
                                                        results[i].GetKey().GetPathGroupId(),
                                                        results[i].GetFIBStatus(),
                                                        results[i].GetOperationID())
                                    }
                                } else {
                                    log.Info("Response: ", results[i])
                                }
                            }
                        } else {
                            /* If we do not expect a Fib response then response is always for RIB */
                            numOperations--
                        }
                    }
                }
        }()

        for _, message := range messages {
            if err = stream.Send(message); err != nil {
                    break
            }
        }
        err = <-errc
        stream.CloseSend()

        return err
}

/* Performs the SLAFGet rpc */
func runSlafGetRequest(conn *grpc.ClientConn, message *pb.SLAFGetMsg,
                       username string, password string) (err error) {

    client := pb.NewSLAFClient(conn)
    ctx, cancel := context.WithTimeout(context.Background(), 600*time.Second)
    ctx = metadata.AppendToOutgoingContext(ctx,
        "username", username, "password", password,
        "iosxr-slapi-clientid", ClientID)
    defer cancel() // make sure all paths cancel the context to avoid context leak

    /* Send the message and receive a unary get rpc back. */
    recvStream, err := client.SLAFGet(ctx, message)
    if err != nil {
        return err
    }

    errc := make(chan error, 1)
    go func() {
        for {
            response, errMsg := recvStream.Recv()
            if errMsg == io.EOF {
                    // read done.
                    close(errc)
                    return
            }
            if errMsg != nil {
                    log.Error(errMsg)
                    errc <- errMsg
                    close(errc)
                    return
            }
            responseStatus := response.GetErrStatus().GetStatus()

            if responseStatus != pb.SLErrorStatus_SL_SUCCESS {
                // Indicate the get operation failed
                errc <- fmt.Errorf("get operation failed for VrfName (%s) and Client (%d) with ErrorStatus: %s",
                                response.GetVrfName(), response.GetClientID(), responseStatus)
            } else {
                // Print out the response message
                log.Info("get operation succeeded for VrfName: ", response.GetVrfName(), " and Client: ", response.GetClientID())
                rspEntry := response.GetAFList()

                for i := 0; i < len(rspEntry); i++ {
                    log.Info("Index: ", i, " for Entry: ", rspEntry[i])
                }
            }
        }
    }()

    err = <-errc
    return err;
}

/* Performs the SlafVrfRegGet rpc */
func runSlafVrfRegGetRequest(conn *grpc.ClientConn, message *pb.SLAFVrfRegGetMsg,
                             username string, password string) (err error) {

    client := pb.NewSLAFClient(conn)
    ctx, cancel := context.WithTimeout(context.Background(), 600*time.Second)
    ctx = metadata.AppendToOutgoingContext(ctx,
        "username", username, "password", password,
        "iosxr-slapi-clientid", ClientID)
    defer cancel() // make sure all paths cancel the context to avoid context leak

    /* Send the message and receive a unary get rpc back. */
    recvStream, err := client.SLAFVrfRegGet(ctx, message)
    if err != nil {
        return err
    }

    errc := make(chan error, 1)
    go func() {
        for {
            response, errMsg := recvStream.Recv()
            if errMsg == io.EOF {
                    // read done.
                    close(errc)
                    return
            }
            if errMsg != nil {
                    log.Error(errMsg)
                    errc <- errMsg
                    close(errc)
                    return
            }
            responseStatus := response.GetErrStatus().GetStatus()

            if responseStatus != pb.SLErrorStatus_SL_SUCCESS {
                // Indicate the get operation failed
                errc <- fmt.Errorf("vrfRegGet operation failed for Client (%d) with ErrorStatus: %s",
                                response.GetClientID(), responseStatus)
            } else {
                // Print out the response message
                log.Info("vrfRegGet operation succeeded for Client: ", response.GetClientID(),
                        " and Table Type: ", response.GetTable())
                rspEntry := response.GetEntries()

                for i := 0; i < len(rspEntry); i++ {
                    log.Info("Index: ", i, " for Entry: ", rspEntry[i])
                }
            }
        }
    }()

    err = <-errc
    return err;
}

/* Performs the SLAFNotifStream rpc */
func runSlafNotifStreamRequest(conn *grpc.ClientConn, notifStreamDuration uint,
                               messages []*pb.SLAFNotifReq, username string, password string) (err error) {

        client := pb.NewSLAFClient(conn)
        ctx, cancel := context.WithTimeout(context.Background(), 600*time.Second)
        ctx = metadata.AppendToOutgoingContext(ctx,
            "username", username, "password", password,
            "iosxr-slapi-clientid", ClientID)
        defer cancel() // make sure all paths cancel the context to avoid context leak

        stream, err := client.SLAFNotifStream(ctx)
        if err != nil {
                return err
        }

        errc := make(chan error, 1)
        go func() {
            for {
                response, errMsg := stream.Recv()
                log.Info("stream: ", response, errMsg)
                if errMsg == io.EOF {
                        // read done.
                        close(errc)
                        return
                }
                if errMsg != nil {
                        log.Error(errMsg)
                        errc <- errMsg
                        close(errc)
                        return
                }

                log.Info("VrfName: ", response.GetVrfName())
                results := response.GetAFNotifs()

                for i := 0; i < len(results); i++ {
                    status := results[i].GetNotifStatus()

                    if status == nil {
                        log.Info("Response: ", results[i])
                    } else {
                        if status.GetNotifStatus().GetStatus() != pb.SLErrorStatus_SL_SUCCESS {
                            errc <- fmt.Errorf("Notification operation failed with ErrorStatus: %s for Request: %s",
                                            status.GetNotifStatus().GetStatus(),
                                            status.GetNotifReq())
                        } else {
                            log.Info("Corresponding Request: ", status.GetNotifReq())
                        }
                    }
                }
            }
        }()

        for _, message := range messages {
            if err = stream.Send(message); err != nil {
                break
            }
        }

        // Keep stream alive for duration client specifies
        time.Sleep(time.Duration(notifStreamDuration) * time.Second)
        stream.CloseSend()
        err = <-errc

        return err
}

/* Function handling the creation and programming of ipv4 routes*/
func RouteOperation(conn *grpc.ClientConn, oper pb.SLObjectOp,
                    routeFlag pb.SLRouteFlags, adminDistance uint32,
                    ackType pb.SLRspACKType, ackPermit pb.SLRspACKPermit,
                    ackCadence pb.SLRspAckCadence,
                    firstPrefix string, prefixLen uint32, numRoutes uint, usePGName string, batchSize uint,
                    nextHopIP string, nexthopInterface string, numPaths uint, autoIncNHIP bool,
                    streamCase bool, username string, password string) {

    var batchIndex uint
    var totalRoutes uint = 0
    var setRoutes uint = 0
    var routeCount uint = 0
    var messages []*pb.SLAFMsg
    var err error = nil
    var pathIndex uint

    /* Initialize some route params */
    prefix := ip4toInt(net.ParseIP(fmt.Sprintf(firstPrefix)))
    nexthop1 := ip4toInt(net.ParseIP(nextHopIP))

    log.Debug("Address: start address: ", prefix,
              ", #numRoutes: ", numRoutes,
              ", #numPaths: ", numPaths,
              ", #batchSize: ", batchSize)

    /* Let's the preparation time it takes to create the messages */
    t0 := time.Now()

    /* Create a message */
    message := &pb.SLAFMsg{
        Oper: oper,
        VrfName: "default",
    }

    /*
    * Populate a batch with batchSize routes each.
    */
    for setRoutes = 1; setRoutes <= numRoutes; setRoutes, prefix = setRoutes+1, incrementIpv4Pfx(prefix, prefixLen) {

        /* Populate the routes' attributes */
        routeIpPtr := &pb.SLAFIPRoute {
            IPRoutePrefix: &pb.SLRoutePrefix{
                Prefix: &pb.SLIpAddress {
                    Address: &pb.SLIpAddress_V4Address{
                        V4Address: prefix,
                    },
                },
                PrefixLen: prefixLen,
            },
            RouteCommon: &pb.SLRouteCommon {
                AdminDistance: adminDistance,
                RouteFlags: []pb.SLRouteFlags{routeFlag,},
            },
        }

        /* We dont need to setup the paths for DELETE*/
        if oper != pb.SLObjectOp_SL_OBJOP_DELETE {
            for pathIndex = 0; pathIndex < numPaths; pathIndex ++ {
                 /* Setup the route's Path 1*/
                p1 := &pb.SLRoutePath{
                }
                if usePGName == "none" {
                    /* Setup the route's Path 1*/
                    p1.NexthopAddress = &pb.SLIpAddress {
                            Address: &pb.SLIpAddress_V4Address{
                                V4Address: nexthop1,
                            },
                        }
                    if len(nexthopInterface) != 0 {
                        p1.NexthopInterface = &pb.SLInterface{
                            Interface: &pb.SLInterface_Name{
                                Name: nexthopInterface,
                            },
                        }
                    }
                } else {
                    // Use already existing path group
                    p1.Entry = &pb.SLRoutePath_PathGroupKey{
                        PathGroupKey: &pb.SLPathGroupRefKey{
                            VrfName: "default",
                            PathGroupId: &pb.SLObjectId{
                                Entry: &pb.SLObjectId_Name{
                                    Name: usePGName,
                                },
                            },
                        },
                    }
                }
                p1.VrfName = "default"

                /*Append to route*/
                routeIpPtr.PathList = append(routeIpPtr.PathList, p1)
                if autoIncNHIP {
                    nexthop1 = nexthop1 + 1
                }
            }
        }

        /* Setup some SLAFOpMsg attributes */
        afObject := &pb.SLAFObject{
            Entry: &pb.SLAFObject_IPRoute{
                IPRoute: routeIpPtr,
            },
        }
        opMsg := &pb.SLAFOpMsg{
            AFObject: afObject,
            OperationID: GlobalOperationID,
            AckType: ackType,
            AckPermits: []pb.SLRspACKPermit{ackPermit,},
            AckCadence: ackCadence,
        }
        GlobalOperationID += 1

        log.Debug("For Prefix: ", prefix,
                  "The OpMsg: ", opMsg);

        /* Append Route to batch */
        message.OpList = append(message.OpList, opMsg)
        routeCount++

        totalRoutes++

        // fmt.Print("Prefix \n", prefix)
        if routeCount == batchSize || routeCount == numRoutes {
            routeCount = 0
            messages = append(messages, message)

            /* After appending clear the message */
            message = &pb.SLAFMsg{
                Oper: oper,
                VrfName: "default",
            }
            batchIndex++
        }
    }

    t1 := time.Now()

    fmt.Printf("%s Total Batches: %d, Routes: %d, Preparation Time: %v\n",
        oper.String(), batchIndex, totalRoutes, t1.Sub(t0))

    if (totalRoutes > 0) {
        var rate float64
        rate = float64(totalRoutes)/(t1.Sub(t0).Seconds())
        fmt.Printf("Preparation Rate: %f\n", rate)
    }

    t0 = time.Now()

    if (streamCase) {
        var fibCheck bool = false
        if int(ackType) != 0 {
            fibCheck = true
        }
        err = runSlafOpStreamRequest(conn, messages,totalRoutes,
            fibCheck, pb.SLTableType_SL_IPv4_ROUTE_TABLE, username, password)
    } else {
        err = runSlafOpRequest(conn, messages,
            pb.SLTableType_SL_IPv4_ROUTE_TABLE, username, password)
    }
    if err != nil {
        log.Fatal(err)
    }

    t1 = time.Now()

    fmt.Printf("%s Total Batches: %d, Routes: %d, ElapsedTime: %v\n",
        oper.String(), batchIndex, totalRoutes, t1.Sub(t0))

    if (totalRoutes > 0) {
        var rate float64
        rate = float64(totalRoutes)/(t1.Sub(t0).Seconds())
        fmt.Printf("Programming Rate: %f\n", rate)
    }
}

/* Function handling the creation and programming of mpls labels */
func LabelOperation(conn *grpc.ClientConn, oper pb.SLObjectOp,
                    mplsFlag pb.SLRouteFlags, adminDistance uint32,
                    ackType pb.SLRspACKType, ackPermit pb.SLRspACKPermit,
                    ackCadence pb.SLRspAckCadence,
                    startLabel uint, startOutLabel uint, numLabels uint,
                    numPaths uint, batchSize uint,
                    nextHopIP string, Interface string, maxIfIdx uint, autoIncNHIP bool,
                    streamCase bool, username string, password string) {

    var err error = nil
    var elspIdx, pathIdx, batchIndex uint
    var numElsps uint = 0
    var sentIlms uint = 0
    var totalIlms uint = 0
    var numIlms uint = 0
    var ilmsInBatch uint = 0
    var messages []*pb.SLAFMsg
    var message = &pb.SLAFMsg{
        Oper: oper,
        VrfName: "default",
    }

    if batchSize == 0 {
        log.Fatalf("Invalid batch size: %d", batchSize)
    }

    log.Debug("Label: start label: ", startLabel,
              ", #labels: ", numLabels,
              ", #numPaths: ", numPaths,
              ", #batchSize: ", batchSize)

    if batchSize > uint(MaxIlmInBatch) {
        batchSize = uint(MaxIlmInBatch)
    }

    /* Initialize some path params */
    nexthop := ip4toInt(net.ParseIP(nextHopIP))

    /* Let's the preparation time it takes to create the messages */
    t0 := time.Now()

    label := startLabel
    numIlms = 1

    totalIlms = numLabels * numIlms
    if batchSize > totalIlms {
        batchSize = totalIlms
    }

    /*
     * Slaf protos currently do not allow elsps to be configured.
     * numElsps:  > 1 for ELSP, 0 otherwise (configured)
     * totalIlms: numLabels * numElsps (calculated)
     * batchSize: number of ilms per batch (configured)
     * numIlms: number of ilms (1 for non ELSP, numElsps otherwise)
     */
    for sentIlms < totalIlms  {

        log.Debug("sentIlms ", sentIlms,
		          " batchIndex ", batchIndex,
		          " ilmsInBatch ", ilmsInBatch,
		          " numIlms ", numIlms,
		          " batchSize ", batchSize,
		          " totalIlms ", totalIlms)

        if ilmsInBatch + numIlms > batchSize && sentIlms != totalIlms {
            batchIndex ++

            messages = append(messages, message)

            ilmsInBatch = 0
        }

        if ilmsInBatch == 0  {
            /* Create a new ILM batch */
            message = &pb.SLAFMsg{
                Oper: oper,
                VrfName: "default",
            }
        }

        /* If we are adding ELSP entries then loop and create as many
         * using the same label. If numElsps is set to 0 we just add
         * one ILM entry for that label.
         */

        for elspIdx = 0; elspIdx < numIlms; elspIdx++   {

            log.Debug("label: ", label, " numIlms: ", numIlms)

            nexthopInterface := ifMunge(Interface, elspIdx, maxIfIdx)
            log.Debug("Interface: ", nexthopInterface)

            /* Setup some of the message object attributes */
            ilm := &pb.SLMplsEntry{
                MplsKey: &pb.SLMplsEntryKey{Label: uint32(label),},
                AdminDistance: adminDistance,
                MplsFlags: []pb.SLRouteFlags{mplsFlag,},
            }

            for pathIdx = 0; pathIdx < numPaths; pathIdx++  {
                nhlfe := &pb.SLRoutePath{
                    NexthopAddress: &pb.SLIpAddress {
                        Address: &pb.SLIpAddress_V4Address{
                            V4Address: nexthop,
                        },
                    },
                }
                if len(nexthopInterface) != 0 {
                    nhlfe.NexthopInterface = &pb.SLInterface{
                        Interface: &pb.SLInterface_Name{
                            Name: nexthopInterface,
                        },
                    }
                }

                if startOutLabel > 0 {
                    outLabel := startOutLabel +
                                (label - startLabel) * numElsps + elspIdx
                    nhlfe.LabelStack = append(nhlfe.LabelStack, uint32(outLabel))
                } else {
                    /* Need an out label for swap */
                    log.Fatalf("Invalid out label")
                }

                /* Append to route */
                ilm.PathList = append(ilm.PathList, nhlfe)
                if autoIncNHIP {
                    nexthop = nexthop + 1
                }
            }

            afObject := &pb.SLAFObject{
                Entry: &pb.SLAFObject_MplsLabel{
                    MplsLabel: ilm,
                },
            }

            opMsg := &pb.SLAFOpMsg{
                AFObject: afObject,
                OperationID: GlobalOperationID,
                AckType: ackType,
                AckPermits: []pb.SLRspACKPermit{ackPermit,},
                AckCadence: ackCadence,
            }
            GlobalOperationID += 1
            /* Append Route to batch */
            message.OpList = append(message.OpList, opMsg)

        }
        sentIlms = sentIlms + numIlms
        if sentIlms >= totalIlms {
            batchIndex ++
            messages = append(messages, message)
            ilmsInBatch = 0
        }
        ilmsInBatch += numIlms
        label++
    }

    t1 := time.Now()

    fmt.Printf("%s Total Batches: %d, Ilms: %d, Preparation time: %v\n",
        oper.String(), batchIndex, sentIlms, t1.Sub(t0))

    if (sentIlms > 0) {
        var rate float64
        rate = float64(sentIlms)/(t1.Sub(t0).Seconds())
        fmt.Printf("Preparation Rate: %f\n", rate)
    }

    t0 = time.Now()

    if (streamCase) {
        var fibCheck bool = false
        if int(ackType) != 0 {
            fibCheck = true
        }
        err = runSlafOpStreamRequest(conn, messages, sentIlms,
            fibCheck, pb.SLTableType_SL_MPLS_LABEL_TABLE, username, password)
    } else {
        err = runSlafOpRequest(conn, messages,
            pb.SLTableType_SL_MPLS_LABEL_TABLE, username, password)
    }

    if err != nil {
        log.Fatal(err)
    }

    t1 = time.Now()


    fmt.Printf("%s Total Batches: %d, Ilms: %d, ElapsedTime: %v\n",
        oper.String(), batchIndex, sentIlms, t1.Sub(t0))

    if (sentIlms > 0) {
        var rate float64
        rate = float64(sentIlms)/(t1.Sub(t0).Seconds())
        fmt.Printf("Programming Rate: %f\n", rate)
    }
}

/* Function handling the creation and programming of pg */
func PGOperation(conn *grpc.ClientConn, oper pb.SLObjectOp,
                 pgFlag pb.SLRouteFlags, adminDistance uint32,
                 ackType pb.SLRspACKType, ackPermit pb.SLRspACKPermit,
                 ackCadence pb.SLRspAckCadence,
                 pgNumRoutes uint, batchSize uint,
                 nextHopIP string, nexthopInterface string, autoIncNHIP bool,
                 streamCase bool, pgName string, username string, password string) {

    var batchIndex uint
    var totalPG uint = 1
    var messages []*pb.SLAFMsg
    var err error = nil
    var count uint = 1

    /* Let's the preparation time it takes to create the messages */
    t0 := time.Now()

    /* Create a message */
    message := &pb.SLAFMsg{
        Oper: oper,
        VrfName: "default",
    }

    pathList := &pb.SLPathGroup_SLPathList {}

    /* We dont need to setup the paths for DELETE*/
    if oper != pb.SLObjectOp_SL_OBJOP_DELETE {
        /* Initialize some route params */
        nexthop1 := ip4toInt(net.ParseIP(nextHopIP))

        for count = 1; count <= pgNumRoutes; count++ {
            /* Populate the routes' attributes for the path group */
            path := &pb.SLRoutePath{
                NexthopAddress: &pb.SLIpAddress {
                    Address: &pb.SLIpAddress_V4Address{
                        V4Address: nexthop1,
                    },
                },
            }
            if len(nexthopInterface) != 0 {
                path.NexthopInterface = &pb.SLInterface{
                    Interface: &pb.SLInterface_Name{
                        Name: nexthopInterface,
                    },
                }
            }
            path.VrfName = "default"
            slPaths := &pb.SLPathGroup_SLPath {
                Path:path,
            }
            pathList.Paths = append(pathList.Paths, slPaths)

            // Increment nexthop1 for another addition of route path
            if autoIncNHIP {
                nexthop1 = nexthop1 + 1
            }
        }
    }

    /* Populate the path group attributes */
    pathGroup := &pb.SLPathGroup {
        PathGroupId: &pb.SLObjectId {
            Entry: &pb.SLObjectId_Name{
                Name:pgName,
            },
        },
        AdminDistance: adminDistance,
        Entry: &pb.SLPathGroup_PathList {
            PathList: pathList,
        },
        PgFlags: []pb.SLRouteFlags{pgFlag,},
    }

    afObject := &pb.SLAFObject{
        Entry: &pb.SLAFObject_PathGroup{
            PathGroup: pathGroup,
        },
    }
    /* Setup some SLAFOpMsg attributes */
    opMsg := &pb.SLAFOpMsg{
        AFObject: afObject,
        OperationID: GlobalOperationID,
        AckType: ackType,
        AckPermits: []pb.SLRspACKPermit{ackPermit,},
        AckCadence: ackCadence,
    }
    GlobalOperationID += 1

    /* Append the opMsg to the SLAFMsg */
    message.OpList = append(message.OpList, opMsg)

    messages = append(messages, message)
    log.Debug("Message structure: ", message)

    t1 := time.Now()

    fmt.Printf("%s Total Batches: %d, Routes: %d, Preparation Time: %v\n",
        oper.String(), batchIndex, totalPG, t1.Sub(t0))

    if (totalPG > 0) {
        var rate float64
        rate = float64(totalPG)/(t1.Sub(t0).Seconds())
        fmt.Printf("Preparation Rate: %f\n", rate)
    }


    t0 = time.Now()

    if (streamCase) {
        var fibCheck bool = false
        if int(ackType) != 0 {
            fibCheck = true
        }
        err = runSlafOpStreamRequest(conn, messages, totalPG,
            fibCheck, pb.SLTableType_SL_PATH_GROUP_TABLE, username, password)
    } else {
        err = runSlafOpRequest(conn, messages,
            pb.SLTableType_SL_PATH_GROUP_TABLE, username, password)
    }
    if err != nil {
        log.Fatal(err)
    }

    t1 = time.Now()

    fmt.Printf("%s Total Batches: %d, Routes: %d, ElapsedTime: %v\n",
        oper.String(), batchIndex, totalPG, t1.Sub(t0))

    if (totalPG > 0) {
        var rate float64
        rate = float64(totalPG)/(t1.Sub(t0).Seconds())
        fmt.Printf("Programming Rate: %f\n", rate)
    }
}

/* Function handling the creation of Get message and rpc call */
func GetOperation(conn *grpc.ClientConn, vrfName string,
                  clientIdAll bool, clientId uint64, tableList pb.SLTableType,
                  routeList bool, vxLanId int, pgRegex string, ipv4Prefix string,
                  ipv4PrefixLen uint32, username string, password string) {

    var err error = nil
    var batchIndex uint

    /* Let's the preparation time it takes to create the messages */
    t0 := time.Now()

    /* Create a message */
    message := &pb.SLAFGetMsg{
        VrfName: vrfName,
    }
    batchIndex++

    // Set up the objects to be search for by the client ids
    if clientIdAll {
        message.Client = &pb.SLAFGetMsg_AllClients{
            AllClients:clientIdAll,
        }
    } else {
        if clientId >= 0 {
            slafClientIdList := &pb.SLAFClientIDList{}
            slafClientIdList.ClientIDList = append(slafClientIdList.ClientIDList, clientId)
            message.Client = &pb.SLAFGetMsg_ClientIDList {
                ClientIDList:slafClientIdList,
            }
        }
    }

    // Set ip the objects to search for based off match
    if routeList {
        routeMatchList := &pb.SLAFGetMatchList{}

        // As these fields are optional, the user may want to set some and not others

        if vxLanId >= 0 {
            getMatch := &pb.SLAFGetMatch{}
            getMatch.Entry = &pb.SLAFGetMatch_VxlanVniId {
                VxlanVniId: uint32(vxLanId),
            }
            routeMatchList.Match = append(routeMatchList.Match, getMatch)
        }

        if pgRegex != "" {
            getMatch := &pb.SLAFGetMatch{}
            getMatch.Entry = &pb.SLAFGetMatch_PathGroupRegex {
                PathGroupRegex: pgRegex,
            }
            routeMatchList.Match = append(routeMatchList.Match, getMatch)
        }

        if ipv4Prefix != "" {
            prefix := ip4toInt(net.ParseIP(fmt.Sprintf(ipv4Prefix)))
            getMatch := &pb.SLAFGetMatch{}
            key := &pb.SLAFObjectKey {
                Key: &pb.SLAFObjectKey_IPRoutePrefix {
                    IPRoutePrefix : &pb.SLRoutePrefix {
                        Prefix: &pb.SLIpAddress {
                            Address: &pb.SLIpAddress_V4Address {
                                V4Address: prefix,
                            },
                        },
                        PrefixLen: ipv4PrefixLen,
                    },
                },
            }
            getMatch.Entry = &pb.SLAFGetMatch_Key {
                Key: key,
            }
            routeMatchList.Match = append(routeMatchList.Match, getMatch)
        }

        message.Match = &pb.SLAFGetMsg_RouteMatchList {
            RouteMatchList: routeMatchList,
        }

    } else {
        if tableList != pb.SLTableType_SL_TABLE_TYPE_RESERVED {
            tableTypeList := &pb.SLTableTypeList{}
            tableTypeList.Table = append(tableTypeList.Table, tableList)
            message.Match = &pb.SLAFGetMsg_TableList {
                TableList : tableTypeList,
            }
        } else {
            log.Debug("Table Type for get message is not set. If on purpose then ignore.")
        }
    }

    t1 := time.Now()

    fmt.Printf("GET Total Batches: %d, Requests: %d, Preparation Time: %v\n",
        batchIndex, 1, t1.Sub(t0))

    var rate float64
    rate = float64(1)/(t1.Sub(t0).Seconds())
    fmt.Printf("Preparation Rate: %f\n", rate)

    t0 = time.Now()

    err = runSlafGetRequest(conn, message, username, password)
    if err != nil {
        log.Fatal(err)
    }

    t1 = time.Now()

    fmt.Printf("GET Total Batches: %d, Requests: %d, ElapsedTime: %v\n",
        batchIndex, 1, t1.Sub(t0))

    rate = float64(1)/(t1.Sub(t0).Seconds())
    fmt.Printf("Request Response Rate: %f\n", rate)
}

/* Function handling the creation of Get message and rpc call */
func VrfRegGetOperation(conn *grpc.ClientConn, username string, password string) {

    var err error = nil
    var batchIndex uint

    /* Let's the preparation time it takes to create the messages */
    t0 := time.Now()

    /* Create a message */
    message := &pb.SLAFVrfRegGetMsg{
        GetAll: true,
    }
    batchIndex++


    t1 := time.Now()

    fmt.Printf("VrfRegGet Total Batches: %d, Requests: %d, Preparation Time: %v\n",
        batchIndex, 1, t1.Sub(t0))

    var rate float64
    rate = float64(1)/(t1.Sub(t0).Seconds())
    fmt.Printf("Preparation Rate: %f\n", rate)

    t0 = time.Now()

    err = runSlafVrfRegGetRequest(conn, message, username, password)
    if err != nil {
        log.Fatal(err)
    }

    t1 = time.Now()

    fmt.Printf("VrfRegGet Total Batches: %d, Requests: %d, ElapsedTime: %v\n",
        batchIndex, 1, t1.Sub(t0))

    rate = float64(1)/(t1.Sub(t0).Seconds())
    fmt.Printf("Request Response Rate: %f\n", rate)
}

/* Function handling the creation of NotifStream message and rpc call */
func NotifStreamOperation(conn *grpc.ClientConn, notifStreamDuration uint,
                          oper pb.SLNotifOp, vrfName string, notifRouteReg bool,
                          srcProto string, srcProtoTag string, tableType pb.SLTableType,
                          nextHopReg bool, ipv4Prefix string, ipv4PrefixLen uint32,
                          exactMatch bool, allowDefault bool, recurse bool,
                          username string, password string) {

    var err error = nil
    var batchIndex uint
    var messages []*pb.SLAFNotifReq

    /* Let's the preparation time it takes to create the messages */
    t0 := time.Now()

    /* Create a message */
    message := &pb.SLAFNotifReq {
        Oper: oper,
        VrfName: vrfName,
    }
    batchIndex++

    // Fill in the Route redistribution registration fields
    if notifRouteReg {
        notifReq := &pb.SLAFNotifRegReq {
            Request: &pb.SLAFNotifRegReq_RedistReq {
                RedistReq : &pb.SLAFRedistRegMsg {
                    SrcProto: srcProto,
                    SrcProtoTag: srcProtoTag,
                    Table: tableType,
                },
            },
            OperationID: GlobalOperationID,
        }
        GlobalOperationID++
        message.NotifReq = append(message.NotifReq,notifReq)
    }

    // Fill in the Next hop registration notificaiton fields
    if nextHopReg {
        prefix := ip4toInt(net.ParseIP(fmt.Sprintf(ipv4Prefix)))
        notifReq := &pb.SLAFNotifRegReq {
            Request: &pb.SLAFNotifRegReq_NextHopReq {
                NextHopReq: &pb.SLAFNextHopRegMsg {
                    NextHopKey: &pb.SLAFNextHopRegKey {
                        Nexthopkey: &pb.SLAFNextHopRegKey_NextHop {
                            NextHop: &pb.SLAFNextHopRegKey_SLNextHopKey {
                                NextHopIP: &pb.SLRoutePrefix {
                                    Prefix: &pb.SLIpAddress {
                                        Address: &pb.SLIpAddress_V4Address{
                                            V4Address: prefix,
                                        },
                                    },
                                    PrefixLen: ipv4PrefixLen,
                                },
                                ExactMatch: exactMatch,
                                AllowDefault: allowDefault,
                                Recurse: recurse,
                            },
                        },
                    },
                },
            },
            OperationID: GlobalOperationID,
        }

        GlobalOperationID++
        message.NotifReq = append(message.NotifReq,notifReq)
    }

    messages = append(messages, message)

    t1 := time.Now()

    fmt.Printf("VrfRegGet Total Batches: %d, Requests: %d, Preparation Time: %v\n",
        batchIndex, len(messages), t1.Sub(t0))

    var rate float64
    rate = float64(len(messages))/(t1.Sub(t0).Seconds())
    fmt.Printf("Preparation Rate: %f\n", rate)

    t0 = time.Now()

    err = runSlafNotifStreamRequest(conn, notifStreamDuration, messages, username, password)
    if err != nil {
        log.Fatal(err)
    }

    t1 = time.Now()

    fmt.Printf("VrfRegGet Total Batches: %d, Requests: %d, ElapsedTime: %v\n",
        batchIndex, len(messages), t1.Sub(t0))

    rate = float64(len(messages))/(t1.Sub(t0).Seconds())
    fmt.Printf("Request Response Rate: %f\n", rate)
}
