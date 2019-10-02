/*
 * Copyright (c) 2016 by cisco Systems, Inc.
 * All rights reserved.
 */
package sl_api

import (
    "fmt"
    "math/big"
    "net"
    "log"
    "time"

    pb "gengo"
    "golang.org/x/net/context"
    "google.golang.org/grpc"
)

func ip4toInt(IPv4Address net.IP) uint32 {
    IPv4Int := big.NewInt(0)
    IPv4Int.SetBytes(IPv4Address.To4())
    return uint32(IPv4Int.Int64())
}

func incrementIpv4Pfx(pfx uint32, prefixLen uint32) (uint32){
    if prefixLen > 32 {
        log.Fatalf("PrefixLen > 32")
    }

    return (pfx + 1<<(32-prefixLen))
}

/* 
 * In this tutorial we send batchNum batches of batchSize each.
 * This basically implies a total of batchNum*batchSize routes will be sent
 *
 * Note: The batch size can not exceed the value of MaxRoutePerRoutemsg
 */
func RouteOperation(conn *grpc.ClientConn, Oper pb.SLObjectOp,
        FirstPrefix string, prefixLen uint32, batchNum uint, batchSize uint,
        NextHopIP string, Interface string) {

    var batchIndex uint
    var totalRoutes int64 = 0

    /* Initialize some route params */
    prefix := ip4toInt(net.ParseIP(fmt.Sprintf(FirstPrefix)))
    nexthop1 := ip4toInt(net.ParseIP(NextHopIP))
    nexthop2 := nexthop1 + 1;

    /* Create a NewSLRoutev4OperClient instance */
    c := pb.NewSLRoutev4OperClient(conn)

    /* Let's compute the time it takes to RPC the routes */
    t0 := time.Now()

    /*
     * Populate a batch with batchSize routes each.
     * Repeat for batchNum batches
     */
    for batchIndex = 0; batchIndex < batchNum; batchIndex++ {
        var response *pb.SLRoutev4MsgRsp = nil
        var err error = nil
        var routeIndex uint

        /* Create a Route batch */
        message := &pb.SLRoutev4Msg{}

        /* Set the VRF Name */
        message.VrfName = "default"

        /* Set the operation */
        message.Oper = Oper

        /* Populate the routes' attributes */
        for routeIndex = 0; routeIndex < batchSize;
            routeIndex, prefix = routeIndex+1, 
                incrementIpv4Pfx(prefix, prefixLen) {

            /* Setup some route attributes */
            route := &pb.SLRoutev4{
                Prefix: prefix,
                PrefixLen: prefixLen,
                RouteCommon: &pb.SLRouteCommon{AdminDistance: 2},
            }

            /* We dont need to setup the paths for DELETE*/
            if Oper != pb.SLObjectOp_SL_OBJOP_DELETE {
                /* Setup the route's Path 1*/
                p1 := &pb.SLRoutePath{
                    NexthopAddress: &pb.SLIpAddress {
                        Address: &pb.SLIpAddress_V4Address{
                            V4Address: nexthop1,
                        },
                    },
                    NexthopInterface: &pb.SLInterface{
                        Interface: &pb.SLInterface_Name{
                            Name: Interface,
                        },
                    },
                }
                /*Append to route*/
                route.PathList = append(route.PathList, p1)

                /* Setup the route's Path 2 (ECMP) */
                p2 := &pb.SLRoutePath{
                    NexthopAddress: &pb.SLIpAddress {
                        Address: &pb.SLIpAddress_V4Address{
                            V4Address: nexthop2,
                        },
                    },
                    NexthopInterface: &pb.SLInterface{
                        Interface: &pb.SLInterface_Name{
                            Name: Interface,
                        },
                    },
                }
                /* Append to route*/
                route.PathList = append(route.PathList, p2)
            }

            /* Append Route to batch */
            message.Routes = append(message.Routes, route)

            totalRoutes++
        }

        /* RPC the message */
        response, err = c.SLRoutev4Op(context.Background(), message)
        if err != nil {
            log.Fatal(err)
        }

        /* Validate response*/
        if response.StatusSummary.Status != pb.SLErrorStatus_SL_SUCCESS {
            fmt.Printf("Route operation failed: %s\n", response)
        }
    }

    t1 := time.Now()

    fmt.Printf("%s Total Batches: %d, Routes: %d, ElapsedTime: %v\n",
        Oper.String(), batchIndex, totalRoutes, t1.Sub(t0))

    if (totalRoutes > 0) {
        var rate float64
        rate = float64(totalRoutes)/(t1.Sub(t0).Seconds())
        fmt.Printf("Rate: %f\n", rate)
    }
}
