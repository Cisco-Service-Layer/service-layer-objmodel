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

    log "github.com/sirupsen/logrus"
)

/* Lindt packages */
import (
    "sl_api"
    "util"
    pb "gengo"
)

var (
    /*
     *   -h for help
     */

    BatchNum = flag.Uint("num_batches", 100,
                         "Number of batches used in the operation")
    BatchSize = flag.Uint("batch_size", 1000,
                          "Number of entries per batch, used in the operation")
    debug     = flag.Bool("debug", false, "Enable debugging")
    Interface = flag.String("interface", "", "Interface name")
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
    RouteOper = flag.Int("route_oper", 0,
                         "Route Operation: Add(1), Update(2), Delete(3)")
    VrfRegOper = flag.Int("vrf_reg_oper", 0,
                         "VRF registration Operation: Reg(1), Unregister(2), EOF(3)")

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
    AutoIncNHIP = flag.Bool("auto_inc_nhip", false,
                         "Auto Increment next hop IP")
    /*
     * For Route Redistribution
     *   - notif Set up channels for ipv4, ipv6 route notifications
     */
    TestGetNotif = flag.Bool("notif", false, "Test route redistribution for ipv4, ipv6 routes using single client")
    UserName = flag.String("username", "", "user name")
    Password = flag.String("password", "", "password")
)

func testMPLSReg(conn *grpc.ClientConn, username string, password string) {
    /* Get MPLS vertical attributes */
    sl_api.MplsGetMsg(conn, username, password)

    /* Perform registration with MPLS vertical */
    sl_api.MplsRegOperation(conn, pb.SLRegOp(*VrfRegOper), username, password)
}

func testMPLS(conn *grpc.ClientConn, username string, password string) {

    if *RouteOper == int(pb.SLObjectOp_SL_OBJOP_ADD) ||
             *RouteOper == int(pb.SLObjectOp_SL_OBJOP_UPDATE) {
        /* Add Label Block Operation */
        sl_api.LabelBlockOperation(conn, pb.SLObjectOp_SL_OBJOP_ADD,
                                   uint32(*startLabel), uint32(*numLabels), *numElsps,
                                   *ClientName, username, password)
    }

    /* Batch Label Operation */
    sl_api.LabelOperation(conn, pb.SLObjectOp(*RouteOper),
                    *startLabel, *startOutLabel, *numLabels, *numPaths,
                    *numElsps, *BatchNum, *BatchSize, *NextHopIP,
                    *Interface, *MaxIfIdx, *AutoIncNHIP, username, password)

    if *RouteOper == int(pb.SLObjectOp_SL_OBJOP_DELETE) {
        /* Delete Label Block Operation */
        sl_api.LabelBlockOperation(conn, pb.SLObjectOp_SL_OBJOP_DELETE,
                                   uint32(*startLabel), uint32(*numLabels),
                                   *numElsps, *ClientName, username, password)
    }
}

func testIPv4Reg(conn *grpc.ClientConn, username string, password string) {
    /* Register VRF */
    sl_api.VrfOperation(conn, pb.SLRegOp(*VrfRegOper), username, password)
}

func testIPv4(conn *grpc.ClientConn, username string, password string) {
    /* Batch Route Operation */
    sl_api.RouteOperation(conn, pb.SLObjectOp(*RouteOper), *FirstPrefix,
        uint32(*PrefixLen), *BatchNum, *BatchSize, *NextHopIP, *Interface,
        *numPaths, *AutoIncNHIP, username, password)
}

func validObjectOp(op int) bool {
    if op == int(pb.SLObjectOp_SL_OBJOP_ADD) ||
       op == int(pb.SLObjectOp_SL_OBJOP_UPDATE) ||
       op == int(pb.SLObjectOp_SL_OBJOP_DELETE) {
       return true
    }

     return false
}

func validVrfReg(op int) bool {
    if op == int(pb.SLRegOp_SL_REGOP_REGISTER) ||
       op == int(pb.SLRegOp_SL_REGOP_UNREGISTER) ||
       op == int(pb.SLRegOp_SL_REGOP_EOF) {
       return true
    }

     return false
}

func testGetNotif(conn *grpc.ClientConn, username string, password string) {
    /* Set up route notif channels for ipv4 and ipv6 routes */
    sl_api.GetNotifChannel(conn, username, password)
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

    if *VrfRegOper != int(pb.SLRegOp_SL_REGOP_RESERVED) &&
       !validVrfReg(*VrfRegOper) {
        log.Fatalf("incorrect vrf reg operation")
        return
    }

    if *RouteOper != int(pb.SLObjectOp_SL_OBJOP_RESERVED) &&
       !validObjectOp(*RouteOper) {
        log.Fatalf("incorrect route operation")
        return
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
    if sl_api.ClientInit(conn, *UserName, *Password) == 0 {
        log.Fatalf("ClientInit error")
        return
    }

    if (*TestMpls) {
        fmt.Printf("Performing MPLS tests\n")
        if validVrfReg(*VrfRegOper) {
            testMPLSReg(conn, *UserName, *Password)
        }
        if validObjectOp(*RouteOper) {
            testMPLS(conn, *UserName, *Password)
        }
    } else {
        fmt.Printf("Performing ipv4 test\n")
        if validVrfReg(*VrfRegOper) {
            fmt.Printf("Performing ipv4 vrf reg\n")
            testIPv4Reg(conn, *UserName, *Password)
        }
        if validObjectOp(*RouteOper) {
            fmt.Printf("Performing route operation\n")
            testIPv4(conn, *UserName, *Password)
        }
    }
    if (*TestGetNotif) {
        fmt.Println("Performing getNotif tests\n")
        testGetNotif(conn, *UserName, *Password)
    }

    /* The process will exit here */
}
