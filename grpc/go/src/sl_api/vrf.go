/*
 * Copyright (c) 2016 by cisco Systems, Inc.
 * All rights reserved.
 */
package sl_api

// Standard packages
import (
    "fmt"
    "log"
    "google.golang.org/grpc"
    "golang.org/x/net/context"
)

// sl api packages
import (
    pb "gengo"
)

func VrfOperation(conn *grpc.ClientConn, oper pb.SLRegOp) {
    /* Create a NewSLRoutev4OperClient instance */
    c := pb.NewSLRoutev4OperClient(conn)

    /* Create a batch of VRF registrations */
    message := &pb.SLVrfRegMsg{}

    /* Set the operation */
    message.Oper = oper

    /* Create a VRF registration object*/
    m1 := &pb.SLVrfReg{
        VrfName:                 "default",
        AdminDistance:           2,
        VrfPurgeIntervalSeconds: 500,
    }

    /* Append VRF registration object to batch */
    message.VrfRegMsgs = append(message.VrfRegMsgs, m1)

    /* RPC the Registration message*/
    response, err := c.SLRoutev4VrfRegOp(context.Background(), message)
    if err != nil {
        log.Fatal(err)
    }

    if response.StatusSummary.Status != pb.SLErrorStatus_SL_SUCCESS {
        log.Fatalf("VRF operation error: %s", response.String())
    }

    fmt.Printf("VRF %s status: %s\n", oper.String(),
        response.StatusSummary.Status.String())
}
