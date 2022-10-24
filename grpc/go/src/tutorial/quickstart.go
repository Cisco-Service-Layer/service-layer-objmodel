/*
 * Copyright (c) 2016 by cisco Systems, Inc.
 * All rights reserved.
 */
package main

/* Standard packages */
import (
    "fmt"
    "google.golang.org/grpc"
    "flag"
    "time"

    log "github.com/sirupsen/logrus"
)

/* Lindt packages */
import (
    "sl_api"
    "util"
    pb "gengo"
)

var (
    /* These can be overriden with command line arguments.
     *
     *   -h for help
     *
     * Common:
     *   -num_batches:  Number of batches to be used in the operation
     *   -batch_size:   The batch size (number of routes, ilms, etc)
     *   -debug:        Enable debugging
     *
     */

    BatchNum = flag.Uint("num_batches", 100,
                         "Number of batches used in the operation")
    BatchSize = flag.Uint("batch_size", 1000,
                          "Number of entries per batch, used in the operation")
    debug     = flag.Bool("debug", false, "Enable debugging")
    Interface = flag.String("interface", "GigabitEthernet0/0/0/0", "Interface name")
    NextHopIP = flag.String("next_hop_ip", "10.0.0.1", "Next Hop IP base address")

    /*
     * For IPv4:
     *   -ipv4:     optional, default
     *
     */
    TestIPv4 = flag.Bool("ipv4", true,
                         "Test IPv4 vertical (default)")
    FirstPrefix = flag.String("first_prefix", "20.0.0.0",
                              "First Prefix to be used in the route operation")
    PrefixLen = flag.Uint("prefix_len", 24,
                          "Prefix Length to be used in the route operation")
    routeOper = flag.Int("route_oper", int(pb.SLObjectOp_SL_OBJOP_ADD),
                         "Route Operation: Add(1), Update(2), Delete(3)")

    /*
     * For MPLS:
     *   -mpls:      Enable MPLS testing
     *   -num_labels: Number of labels to be reserved
     *   -num_paths: Number of paths to add per ILM entry
     *   -num_elsps: Number of ELSP entries to be added per label
     *
     */
    TestMpls = flag.Bool("mpls", false, "Test MPLS vertical")
    startLabel = flag.Uint("start_label", 12000, "Starting label")
    startOutLabel = flag.Uint("start_out_label", 20000, "Starting out label")
    numLabels = flag.Uint("num_labels", 1000, "Number of labels")
    numPaths = flag.Uint("num_paths", 1, "Number of paths")
    numElsps = flag.Uint("num_elsps", 0,
                         "Number of ELSP entries (0 - 9, 0: no-elsp (default), 9: elsp-dflt)")
    MaxIfIdx  = flag.Uint("max_if_idx", 0,
                          "Increment the last index of the interface name for each elsp up to this number")
    ClientName = flag.String("client_name", "Service-layer",
                             "The client name to be used during MPLS CBF label block allocation")
)

func testMPLS(conn *grpc.ClientConn) {
    /* Get MPLS vertical attributes */
    sl_api.MplsGetMsg(conn)

    /*
     * Perform registration with MPLS vertical only for ADD operation. Ideally
     * this tool should have provided options for reg/object add/eof, but for
     * now make it easy for user to perform an implicit register on ADD
     */
    if pb.SLObjectOp(*routeOper) == pb.SLObjectOp_SL_OBJOP_ADD {
       /* MPLS Registration and EOF to flush old entries */
       sl_api.MplsRegOperation(conn, pb.SLRegOp_SL_REGOP_REGISTER)

       /* flush on add of new labels */
        sl_api.MplsRegOperation(conn, pb.SLRegOp_SL_REGOP_EOF)
        time.Sleep(5 * time.Second)

        /* Batch Label Block Operation */
        sl_api.LabelBlockOperation(conn, pb.SLObjectOp(*routeOper),
                                   uint32(*startLabel), uint32(*numLabels), *numElsps,
                                   *ClientName)
    }

    /* Batch Label Operation */
    sl_api.LabelOperation(conn, pb.SLObjectOp(*routeOper),
                    *startLabel, *startOutLabel, *numLabels, *numPaths,
                    *numElsps, *BatchNum, *BatchSize, *NextHopIP,
                    *Interface, *MaxIfIdx)
}

func testIPv4(conn *grpc.ClientConn) {
    /* Register VRF */
    sl_api.VrfOperation(conn, pb.SLRegOp_SL_REGOP_REGISTER)

    /* Send EOF for VRF */
    sl_api.VrfOperation(conn, pb.SLRegOp_SL_REGOP_EOF)

    /* Batch Route Operation */
    sl_api.RouteOperation(conn, pb.SLObjectOp(*routeOper), *FirstPrefix,
        uint32(*PrefixLen), *BatchNum, *BatchSize, *NextHopIP, *Interface)
}

func main() {
    /* Parse any command line arguments */
    flag.Parse()

    if *debug {
        log.SetLevel(log.DebugLevel)
        log.Debug("Debug level is enabled")
    }

    if *numElsps > 9 {
        log.Fatal("Invalid number of ELSPs")
    }

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

    if (*TestMpls) {
        testMPLS(conn)
    } else {
        testIPv4(conn)
    }

    /* The process will exit here */
}
