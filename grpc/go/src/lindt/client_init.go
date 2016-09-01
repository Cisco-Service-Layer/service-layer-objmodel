/*
 * Copyright (c) 2016 by cisco Systems, Inc.
 * All rights reserved.
 */
package lindt

/* Standard packages */
import (
    "fmt"
    "log"
    "google.golang.org/grpc"
    "golang.org/x/net/context"
)

/* Lindt packages */
import (
    pb "gengo"
)

func ClientInit(conn *grpc.ClientConn) (int) {
    /* Setup a go-routine channel to synchronize both go-routines*/
    sync_chan := make(chan int)

    /* Setup the notification channel */
    go setupNotifChannel(conn, sync_chan)

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

    /* RPC to Get the globals. */
    response, err := globalClient.SLGlobalsGet(context.Background(),
        globalGetMsg)
    if err != nil {
        fmt.Println("Client Error %v", err)
        return 0
    }

    /* Print Server response */
    fmt.Println("Client INIT Server response: ",
            response.ErrStatus.Status)
    fmt.Println("Max VRF Name Len     : ", response.MaxVrfNameLength)
    fmt.Println("Max Iface Name Len   : ", response.MaxInterfaceNameLength)
    fmt.Println("Max Paths per Entry  : ", response.MaxPathsPerEntry)
    fmt.Println("Max Prim per Entry   : ", response.MaxPrimaryPathPerEntry)
    fmt.Println("Max Bckup per Entry  : ", response.MaxBackupPathPerEntry)
    fmt.Println("Max Labels per Entry : ", response.MaxMplsLabelsPerPath)
    fmt.Println("Min Prim Path-id     : ", response.MinPrimaryPathIdNum)
    fmt.Println("Max Prim Path-id     : ", response.MaxPrimaryPathIdNum)
    fmt.Println("Min Bckup Path-id    : ", response.MinBackupPathIdNum)
    fmt.Println("Max Bckup Path-id    : ", response.MaxBackupPathIdNum)
    fmt.Println("Max Remote Bckup Addr: ", response.MaxRemoteAddressNum)

    return wait_resp
}

func setupNotifChannel(conn *grpc.ClientConn, sync_chan chan int) {
    /* Create a sLGlobalClient instance */
    globalClient := pb.NewSLGlobalClient(conn)

    /* Create a SLGlobalsGetMsg */
    initMsg := &pb.SLInitMsg {
        MajorVer: uint32(pb.SLVersion_SL_MAJOR_VERSION),
        MinorVer: uint32(pb.SLVersion_SL_MINOR_VERSION),
        SubVer: uint32(pb.SLVersion_SL_SUB_VERSION),
    }

    /* RPC to Init the notification channel */
    stream, err := globalClient.SLGlobalInitNotif(context.Background(),
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
