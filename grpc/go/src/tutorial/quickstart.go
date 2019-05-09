/*
 * Copyright (c) 2016 by cisco Systems, Inc.
 * All rights reserved.
 */
package main

/* Standard packages */
import (
    "fmt"
    "log"
    "google.golang.org/grpc"
    "flag"
)

/* Lindt packages */
import (
    "sl_api"
    "util"
    pb "gengo"
)

var (
    /*These can be overriden from the command line argument. -h for help*/
    routeOper = flag.Int("route_oper", int(pb.SLObjectOp_SL_OBJOP_ADD),
        "Route Operation Add(1), Update(2), Delete(3)")
    FirstPrefix = flag.String("first_prefix", "20.0.0.0",
        "First Prefix to be used in the route operation")
    PrefixLen = flag.Uint("prefix_len", 24,
        "Prefix Length to be used in the route operation")
    BatchNum = flag.Uint("batch_num", 100,
        "Number of batched used in the route operation")
    BatchSize = flag.Uint("batch_size", 1000,
        "Number of routes per batch, used in the route operation")
)

func main() {
    /* Parse any command line arguments */
    flag.Parse()

    /* Get Server IP and Port from Env */
    server,port := util.GetServerIPPort()
    address := fmt.Sprintf("%s:%s", server, port)

    /* Setup the connection with the server */
    conn, err := grpc.Dial(address, grpc.WithInsecure())
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    /* Initialize and handshake with server */
    if sl_api.ClientInit(conn) == 0 {
        log.Fatalf("ClientInit error")
        return
    }

    /* Register VRF */
    sl_api.VrfOperation(conn, pb.SLRegOp_SL_REGOP_REGISTER)

    /* Send EOF for VRF */
    sl_api.VrfOperation(conn, pb.SLRegOp_SL_REGOP_EOF)

    /* Batch Route Operation */
    sl_api.RouteOperation(conn, pb.SLObjectOp(*routeOper), *FirstPrefix,
        uint32(*PrefixLen), *BatchNum, *BatchSize)

    /*The process will exit here*/
}
