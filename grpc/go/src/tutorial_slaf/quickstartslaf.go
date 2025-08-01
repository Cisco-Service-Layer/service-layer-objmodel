/*
 * Copyright (c) 2025 by cisco Systems, Inc.
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
    "sl_api_slaf"
    "util"
    pb "gengo"
)

var (
    /*
     *   Required for connection
     */
    Username = flag.String("username", "", "user name")
    Password = flag.String("password", "", "password")

    /*
     *   -h for help
     */

    /*
     * Optional Fields:
     */
    Debug           = flag.Bool("debug", false, "Enable debugging")
    PrintResponse   = flag.Bool("print_responses", false, "Prints the responses")

    /*
     *   Used for route programming in conjunction with ipv4,mpls,or pg fields below Showcases how to set and perform SLAFOp and SLAFOpStream rpc's.
     */
    StreamCase      = flag.Bool("stream_case", false, "Use the streaming rpc for route programming in SLAF")

    BatchSize       = flag.Uint("batch_size", 1000,
                        "Number of entries per batch, used in the operation")
    Interface       = flag.String("interface", "FourHundredGigE0/0/0/0", "Interface name")
    NextHopIP       = flag.String("next_hop_ip", "10.0.0.1", "Next Hop IP base address")
    AutoIncNHIP     = flag.Bool("auto_inc_nhip", false,
                        "Auto Increment next hop IP")
    AdminDistance   = flag.Int("admin_distance", 99, "Admin Distance")
    AckType         = flag.Int("ack_type", 0,
                        "Types of Acknowledgement agent expects: RIB_ACK(0), RIB_AND_FIB_ACK(1), RIB_FIB_INUSE_ACK(2)")
    AckPermit       = flag.Int("ack_permit", 0,
                        `Response types permitted: SL_PERMIT_FIB_STATUS_ALL(0), SL_PERMIT_FIB_SUCCESS(1),
                        SL_PERMIT_FIB_FAILED(2), SL_PERMIT_FIB_INELIGIBLE(3), SL_PERMIT_FIB_INUSE_SUCCESS(4)`)
    AckCadence      = flag.Int("ack_cadence", 0,
                        `Cadence of hw programming responses: SL_RSP_CONTINUOUS(0), SL_RSP_JUST_ONCE(1),
                        SL_RSP_ONCE_EACH(2), SL_RSP_NONE(3)`)
    RouteOper       = flag.Int("route_oper", 0,
                        "Route Operation: Add(1), Update(2), Delete(3)")
    VrfRegOper      = flag.Int("vrf_reg_oper", 0,
                        "VRF registration Operation: Reg(1), Unregister(2), EOF(3)")
    SLRouteFlag      = flag.Int("route_flag", 0,
                        `Control programming of the route/PG to RIB: SL_ROUTE_FLAG_RESERVED(0), SL_ROUTE_FLAG_PREFER_OVER_LDP(1),
                        SL_ROUTE_FLAG_DISABLE_LABEL_MERGE(2), SL_ROUTE_FLAG_VIABLE_PATHS_ONLY(3), SL_ROUTE_FLAG_ACTIVE_ON_VIABLE_PATH(4)`)
    /*
     * For Programming IPv4 routes:
     *   -ipv4:     Enable Ipv4 testing. Used in conjunction with the route programming fields.
     *
     */
    TestIPv4        = flag.Bool("ipv4", false,
                        "Test IPv4 vertical")
    FirstPrefix     = flag.String("first_prefix", "20.0.0.0",
                        "First Prefix to be used in the route operation")
    PrefixLen       = flag.Uint("prefix_len", 24,
                        "Prefix Length to be used in the route operation")
    RouteNum        = flag.Uint("num_routes", 100,
                        "Number of routes used in the operation")
    UsePG           = flag.String("use_pg_for_ipv4", "none",
                        "The path group to use for programming ipv4 routes")

    /*
     * For Programming MPLS labels:
     *   -mpls:      Enable MPLS testing. Used in conjunction with the route programming fields.
     *
     */
    TestMpls        = flag.Bool("mpls", false, "Test MPLS vertical")
    StartLabel      = flag.Uint("start_label", 12000, "Starting label")
    OutLabel        = flag.Uint("out_label", 20000, "Out label")
    NumLabels       = flag.Uint("num_labels", 1000, "Number of labels")
    NumPaths        = flag.Uint("num_paths", 1, "Number of paths")
    MaxIfIdx        = flag.Uint("max_if_idx", 0,
                        "Increment the last index of the interface name for each elsp up to this number")

    /*
     *For Programming PG:
     * -create_path_group:      Enable PG Testing and provide a name for the PG. For purposes of this tutorial, we showcase how to create pg for ipv4 routes.
     *                          When set, will use NextHopIP and Interface variables for information to create the pathgroup.
     *
     */
    TestPG      = flag.Bool("pg", false, "Test PG creation")
    PGName      = flag.String("pg_name", "default", "PathGroup Name")
    PGNumRoutes = flag.Uint("pg_num_path", 1, "Number of Route paths to add into path group")

    /*
     * For Get:
     * -get:    Enable Get Testing. Showcases how to set up and perform SLAFGet Rpc.
     *          The messaged request associated with this rpc can handle multiple different objects,
     *          but for this tutorial we showcase how to set one of each type in any repeated field of the request.
     *
     */
    TestGet         = flag.Bool("get", false, "Test Get Request")
    VrfName         = flag.String("get_vrf_name", "default", "VrfName for object search")
    ClientIDAll     = flag.Bool("get_client_id_all", false, "Indicates User wants to return objects produced by all client ids")
    ClientID        = flag.Int("get_client_id", 521, "Indicates User wants to return objects produced by specific client id")
    TableList       = flag.Int("get_table_list", 0,
                        `Indicates the Table types the user wishes to search for Table type:
                        SL_TABLE_TYPE_RESERVED(0), SL_IPv4_ROUTE_TABLE(1), SL_IPv6_ROUTE_TABLE(2), SL_MPLS_LABEL_TABLE(3), SL_PATH_GROUP_TABLE(4)`)
    GetRouteList    = flag.Bool("get_route_list", false, `Indicates user wishes to search based on any of the GetRouteList criteria below.
                                                      If set, will override the table_list`)
    VxLanID         = flag.Int("get_vxlanid", -1, "This is a GetRouteList field. Using VxLanID for object search")
    PgRegex         = flag.String("get_pg_regex", "", "This is a GetRouteList field. Using Path Group Regex expression for object search")
    GetIpv4Prefix   = flag.String("get_ipv4_prefix", "",
                        "This is a GetRouteList field and used in conjunction with get_ipv4_prefix_len. Using ipv4 prefix and prefix len for object search")
    GetIpv4PrefixLen = flag.Int("get_ipv4_prefix_len", 24,
                        "This is a GetRouteList field and used in conjunction with get_ipv4_prefix. Using ipv4 prefix and len for object search")

     /*
     * For GetRegVrf:
     * -get_reg_vrf:     Enable Get Vrf Testing. Showcases how to set up and perform SLAFNotifStream rpc.
     *
     */
    TestGetRegVrf = flag.Bool("get_reg_vrf", false, "Test GetVrf Request ")

    /*
     * For NotifStream:
     * -notif_stream:     Enable Notification Stream Testing. Showcases how to set up and perform SLAFGetVrf rpc.
     *                    The messaged request associated with this rpc can handle multiple different objects,
     *                    but for this tutorial we showcase how to set one of each type in any repeated field of the request.
     *                    Also, we showcase how to setup notification route lists for only ipv4 routes.
     *
     */
    TestNotifStream     = flag.Bool("notif_stream", false, "Test NotifStream")
    NotifStreamDuration = flag.Uint("notif_duration", 10, "Duration of time (seconds) that the user wants to keep the stream alive for")
    NotifOper           = flag.Uint("notif_oper", 0, `This is to enable or disable route notifications in a vrf or next hop change.
                            The choices are: SL_NOTIFOP_RESERVED(0), SL_NOTIFOP_ENABLE(1) or SL_NOTIFOP_DISABLE(2)`)
    NotifVrfname        = flag.String("notif_vrfname", "default", "Vrf the client is interested in")
    NotifRouteReg       = flag.Bool("notif_route_reg", false, `This is to indicate the client wants to do Route redistribution registration.
                            This option requires setting the NotifRouteReg fields below`)
    NotifSrcProto       = flag.String("notif_route_src_proto", "", `This is a NotifRouteReg field.
                            For route redistribution registration for routes with specified source protocol`)
    NotifSrcProtoTag    = flag.String("notif_route_src_proto_tag", "", `This is a NotifRouteReg field .
                            For route redistribution registration for routes with specified source protocol tags`)
    NotifTableType      = flag.Int("notif_route_table_type", 0,
                            `This is a NotifRouteReg field. Indicate the Table types the user wishes to search for table type:
                            SL_TABLE_TYPE_RESERVED(0), SL_IPv4_ROUTE_TABLE(1), SL_IPv6_ROUTE_TABLE(2), SL_MPLS_LABEL_TABLE(3), SL_PATH_GROUP_TABLE(4)`)
    NotifNextHopReg     = flag.Bool("notif_next_hop_reg", false, `This is to indicate client wants to do next hop notification registration.
                            For this tutorial we showcase how to do this for ipv4 routes.
                            This option requires setting the NotifNextHopReg fields below:`)
    NotifIpv4Prefix     = flag.String("notif_ipv4_prefix", "20.0.0.0", "This is a NotifNextHopReg field")
    NotifIpv4PrefixLen  = flag.Int("notif_ipv4_prefix_len", 24, "This is a NotifNextHopReg field")
    NotifExactMatch     = flag.Bool("notif_exact_match", false, `This is a NotifNextHopReg field.
                            Choose to do exact match (true), or best match (false)`)
    NotifAllowDefault   = flag.Bool("notif_allow_default", false, `This is a NotifNextHopReg field.
                            Allows default route to be returned`)
    NotifRecurse        = flag.Bool("notif_recurse", false, `This is a NotifNextHopReg field.
                            Return all path list of nexthops (true) or immediately viable path list (false)`)
)


func testMPLSRegSlaf(conn *grpc.ClientConn, Username string, Password string) {

    /* Perform registration with MPLS vertical */
    sl_api_slaf.SlafVrfRegOperation(conn, pb.SLRegOp(*VrfRegOper), pb.SLTableType(pb.SLTableType_SL_MPLS_LABEL_TABLE), Username, Password)
}

func testMPLSSlaf(conn *grpc.ClientConn, Username string, Password string) {

    sl_api_slaf.LabelOperation(conn, pb.SLObjectOp(*RouteOper),
                               pb.SLRouteFlags(*SLRouteFlag), uint32(*AdminDistance),
                               pb.SLRspACKType(*AckType), pb.SLRspACKPermit(*AckPermit),
                               pb.SLRspAckCadence(*AckCadence), *StartLabel,
                               *OutLabel, *NumLabels, *NumPaths,
                               *BatchSize, *NextHopIP,
                               *Interface, *MaxIfIdx, *AutoIncNHIP,
                               *StreamCase, Username, Password)
}

func testIPv4RegSlaf(conn *grpc.ClientConn, Username string, Password string) {
    /* Perform registration with IPV4 vertical */
    sl_api_slaf.SlafVrfRegOperation(conn, pb.SLRegOp(*VrfRegOper),
                                    pb.SLTableType(pb.SLTableType_SL_IPv4_ROUTE_TABLE),
                                    Username, Password)
}

func testIPv4Slaf(conn *grpc.ClientConn, Username string, Password string) {

    sl_api_slaf.RouteOperation(conn, pb.SLObjectOp(*RouteOper),
                               pb.SLRouteFlags(*SLRouteFlag), uint32(*AdminDistance),
                               pb.SLRspACKType(*AckType), pb.SLRspACKPermit(*AckPermit),
                               pb.SLRspAckCadence(*AckCadence), *FirstPrefix,
                               uint32(*PrefixLen), *RouteNum, *UsePG, *BatchSize, *NextHopIP, *Interface,
                               *NumPaths, *AutoIncNHIP,
                               *StreamCase, Username, Password)
}

func testPGRegSlaf(conn *grpc.ClientConn, Username string, Password string) {
    /* Perform registration with MPLS vertical */
    sl_api_slaf.SlafVrfRegOperation(conn, pb.SLRegOp(*VrfRegOper), pb.SLTableType(pb.SLTableType_SL_PATH_GROUP_TABLE), Username, Password)
}

func testPGSlaf(conn *grpc.ClientConn, Username string, Password string) {

    sl_api_slaf.PGOperation(conn, pb.SLObjectOp(*RouteOper),
                            pb.SLRouteFlags(*SLRouteFlag), uint32(*AdminDistance),
                            pb.SLRspACKType(*AckType), pb.SLRspACKPermit(*AckPermit),
                            pb.SLRspAckCadence(*AckCadence), *PGNumRoutes, *BatchSize, *NextHopIP,
                            *Interface, *AutoIncNHIP, *StreamCase, *PGName,
                            Username, Password)
}

func testGetSlaf(conn *grpc.ClientConn, Username string, Password string) {

    sl_api_slaf.GetOperation(conn, *VrfName, *ClientIDAll, uint64(*ClientID),
                             pb.SLTableType(*TableList), *GetRouteList, *VxLanID, *PgRegex, *GetIpv4Prefix,
                             uint32(*GetIpv4PrefixLen), Username, Password)
}

func testVrfRegGetSlaf(conn *grpc.ClientConn, Username string, Password string) {

    sl_api_slaf.VrfRegGetOperation(conn, Username, Password)
}

func testNotifStream(conn *grpc.ClientConn, Username string, Password string) {

    sl_api_slaf.NotifStreamOperation(conn, *NotifStreamDuration, pb.SLNotifOp(*NotifOper), *NotifVrfname,
                                     *NotifRouteReg, *NotifSrcProto, *NotifSrcProtoTag, pb.SLTableType(*NotifTableType),
                                     *NotifNextHopReg, *NotifIpv4Prefix, uint32(*NotifIpv4PrefixLen),
                                     *NotifExactMatch, *NotifAllowDefault, *NotifRecurse, Username, Password)
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

func main() {
    /* Parse any command line arguments */
    flag.Parse()

    // Print any level of Warn and higher with log
    log.SetLevel(log.WarnLevel)

    if *PrintResponse {
        log.SetLevel(log.InfoLevel)
        log.Debug("Info level is enabled")
    }

    if *Debug {
        log.SetLevel(log.DebugLevel)
        log.Debug("Debug level is enabled")
    }

    if *Username == "" || *Password == "" {
        log.Info("Username and/or Password was left empty")
    }
    var route_programming_set bool = *TestIPv4 || *TestMpls || *TestPG

    if route_programming_set {
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
    if sl_api_slaf.ClientInit(conn, *Username, *Password) == 0 {
        log.Fatalf("ClientInit error")
        return
    }

    /* Checks for some message restrictions */
    if len(*VrfName) > int(sl_api_slaf.MaxVrfNameLength) {
        log.Fatalf("get_vrf_name is too long!")
    }
    if len(*NotifVrfname) > int(sl_api_slaf.MaxVrfNameLength) {
        log.Fatalf("notif_vrfname is too long!")
    }
    if len(*Interface) > int(sl_api_slaf.MaxInterfaceNameLength) {
        log.Fatalf("Interface name is too long!")
    }

    if uint32(*BatchSize) > sl_api_slaf.MaxBatchSize {
        *BatchSize = uint(sl_api_slaf.MaxBatchSize)
        log.Warn("Batch size was above the max. It is now updated to the max batch size")
    }
    if uint32(*NumPaths) > sl_api_slaf.MaxPrimaryPathPerEntry {
        *NumPaths = uint(sl_api_slaf.MaxPrimaryPathPerEntry)
        log.Warn("Primary path per entry was above the max. It is now updated to the max amount")
    }
    if uint32(*PGNumRoutes) > sl_api_slaf.MaxPrimaryPathPerEntry {
        *PGNumRoutes = uint(sl_api_slaf.MaxPrimaryPathPerEntry)
        log.Warn("Primary path per entry was above the max. It is now updated to the max amount")
    }

    if route_programming_set {
        if *TestMpls {
            fmt.Printf("Performing MPLS tests\n")
            if validVrfReg(*VrfRegOper) {
                testMPLSRegSlaf(conn, *Username, *Password)
            }
            if validObjectOp(*RouteOper) {
                testMPLSSlaf(conn, *Username, *Password)
            }
        } else if *TestIPv4 {
            fmt.Printf("Performing ipv4 tests\n")
            if validVrfReg(*VrfRegOper) {
                fmt.Printf("Performing ipv4 vrf reg\n")
                testIPv4RegSlaf(conn, *Username, *Password)
            }
            if validObjectOp(*RouteOper) {
                fmt.Printf("Performing route operation\n")
                testIPv4Slaf(conn, *Username, *Password)
            }
        } else if *TestPG {
            fmt.Printf("Performing PG test\n")
            if validVrfReg(*VrfRegOper) {
                testPGRegSlaf(conn, *Username, *Password)
            }
            if validObjectOp(*RouteOper) {
                testPGSlaf(conn, *Username, *Password)
            }
        } else {
            log.Fatalf("Route Programming is set, but the table type is not set to an accepted value")
        }
    } else {
        if *TestGet {
            fmt.Printf("Performing Get test\n")
            testGetSlaf(conn, *Username, *Password)
        }

        if *TestGetRegVrf {
            fmt.Printf("Performing Get Registered Vrf test\n")
            testVrfRegGetSlaf(conn, *Username, *Password)
        }
    }


    if (*TestNotifStream) {
        fmt.Println("Performing NotifStream tests\n")
        testNotifStream(conn, *Username, *Password)
    }

    /* The process will exit here */
}
