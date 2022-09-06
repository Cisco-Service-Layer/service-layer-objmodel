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

// runSLAv4Request streams IPv4 SL-API object to router.
func runSLAv4Request(conn *grpc.ClientConn, messages []*pb.SLRoutev4Msg) error {
        client := pb.NewSLRoutev4OperClient(conn)
        ctx, cancel := context.WithTimeout(context.Background(), 600*time.Second)
        defer cancel() // make sure all paths cancel the context to avoid context leak

        stream, err := client.SLRoutev4OpStream(ctx)
        if err != nil {
                return err
        }
        waitc := make(chan struct{})
        go func() (err error) {
                for {
                        response, err := stream.Recv()
                        if response == nil {
                                // read done.
                                close(waitc)
                                return nil
                        }
                        if err != nil {
                                return err
                        }
                        if response.StatusSummary.Status != pb.SLErrorStatus_SL_SUCCESS {
                                return fmt.Errorf("route operation failed: %s", response)
                        }
                }
        }()
        for _, message := range messages {
                if err = stream.Send(message); err != nil {
                        return err
                }
        }
        stream.CloseSend()
        <-waitc
        return nil
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
    var messageGroup []*pb.SLRoutev4Msg
    var err error = nil

    /* Initialize some route params */
    prefix := ip4toInt(net.ParseIP(fmt.Sprintf(FirstPrefix)))
    nexthop1 := ip4toInt(net.ParseIP(NextHopIP))
    nexthop2 := nexthop1 + 1;

    /* Create a NewSLRoutev4OperClient instance */
    // c := pb.NewSLRoutev4OperClient(conn)

    /* Let's compute the time it takes to RPC the routes */
    t0 := time.Now()

    /*
     * Populate a batch with batchSize routes each.
     * Repeat for batchNum batches
     */
    for batchIndex = 0; batchIndex < batchNum; batchIndex++ {
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

        messageGroup = append(messageGroup, message)
    }

    t1 := time.Now()

    fmt.Printf("%s Total Batches: %d, Routes: %d, Preparation Time: %v\n",
        Oper.String(), batchIndex, totalRoutes, t1.Sub(t0))

    if (totalRoutes > 0) {
        var rate float64
        rate = float64(totalRoutes)/(t1.Sub(t0).Seconds())
        fmt.Printf("Preparation Rate: %f\n", rate)
    }

    t0 = time.Now()

    err = runSLAv4Request(conn, messageGroup)
    if err != nil {
        fmt.Printf("Route send failed %s", err)
    }

    t1 = time.Now()

    fmt.Printf("%s Total Batches: %d, Routes: %d, ElapsedTime: %v\n",
        Oper.String(), batchIndex, totalRoutes, t1.Sub(t0))

    if (totalRoutes > 0) {
        var rate float64
        rate = float64(totalRoutes)/(t1.Sub(t0).Seconds())
        fmt.Printf("Programming Rate: %f\n", rate)
    }
}
