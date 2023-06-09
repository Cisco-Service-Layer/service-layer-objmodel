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
    "io"
    "sync"
    "encoding/json"
    "errors"
    "encoding/binary"

    pb "gengo"
    "golang.org/x/net/context"
    "google.golang.org/grpc"
)

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

func byte2ip6(IPV6Address []byte) net.IP {
    var ip net.IP = IPV6Address 
    return ip
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
        errc := make(chan error, 1)
        go func() {
                for {
                        response, err := stream.Recv()
                        if response == nil {
                                // read done.
                                close(errc)
                                return
                        }
                        if err != nil {
                                errc <- err
                                return
                        }
                        if response.StatusSummary.Status != pb.SLErrorStatus_SL_SUCCESS {
                                errc <- fmt.Errorf("route operation failed: %s", response)
                                close(errc)
                                return
                        }
                }
        }()
        for _, message := range messages {
                if err = stream.Send(message); err != nil {
                        return err
                }
        }
        stream.CloseSend()
        err = <-errc
        return err
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
        NextHopIP string, Interface string, numPaths uint, AutoIncNHIP bool) {

    var batchIndex uint
    var totalRoutes int64 = 0
    var messageGroup []*pb.SLRoutev4Msg
    var err error = nil
    var pathIndex uint

    /* Initialize some route params */
    prefix := ip4toInt(net.ParseIP(fmt.Sprintf(FirstPrefix)))
    nexthop1 := ip4toInt(net.ParseIP(NextHopIP))

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
                for pathIndex = 0; pathIndex < numPaths; pathIndex ++ {
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
                    if AutoIncNHIP {
                        nexthop1 = nexthop1 + 1
                    }
                }
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

func GetNotifChannel(conn *grpc.ClientConn) {
    var err error
    var wg sync.WaitGroup
    /* Take the lock to make sure console output for notif and parse IPs of each notif
     * are not intermingled with other RPC's go routine.
     */
    var lck sync.Mutex
    wg.Add(2)
    ctx, cancel := context.WithTimeout(context.Background(), time.Duration(240*time.Second))
    defer cancel() // Release resources if we exit before timeout 
    var msgs1  = []*pb.SLRouteGetNotifMsg {
                                 constructNotifmsg(1, "default", "local", ""),
				 constructNotifmsg(2, "default", "connected", ""),
				 constructNotifmsg(3, "default", "static", "")}
    var msgs2  = []*pb.SLRouteGetNotifMsg {
                                 constructNotifmsg(1, "default", "local", ""),
                                 constructNotifmsg(2, "default", "connected", ""),
			         constructNotifmsg(3, "default", "static", "")} 
    /* Note: 
     - Deadline Exceeded is not an error.
       It essentially means client is not interested in notifcation anymore.
     - log.Fatal will log error and exit program. Avoid using it unless necessary.
     */
    go func() { 
        err = getNotifv4(conn, ctx, msgs1, &wg, &lck)
	if err != nil {
	    log.Print(err)
	}
    }()
    go func() {
	err = getNotifv6(conn, ctx, msgs2, &wg, &lck)
	if err != nil {
            log.Print(err)
        }
    }()
    wg.Wait()
    log.Print("v4 and v6 getNotif RPC  exited")
    return

}

func constructNotifmsg(seqno uint64, vrf_name, src_proto, src_proto_tag string) *pb.SLRouteGetNotifMsg {

    msg := &pb.SLRouteGetNotifMsg{
        Oper : pb.SLNotifOp_SL_NOTIFOP_ENABLE,
        Correlator : seqno,
	VrfName : vrf_name,
	SrcProto : src_proto,
	SrcProtoTag : src_proto_tag,
    }
    return msg
}

func getNotifv4(conn *grpc.ClientConn, ctx context.Context, msgs []*pb.SLRouteGetNotifMsg, wg *sync.WaitGroup, lck *sync.Mutex) error {

    defer wg.Done()

    errCh := make(chan error, 1)

    client := pb.NewSLRoutev4OperClient(conn)
    stream, err := client.SLRoutev4GetNotifStream(ctx)
    if err != nil {
	    log.Fatalf("v4: getNotif Could not get stream from client. Exit RPC error  %v", err)
            return err
    }

    go func() {
        log.Print("v4: getNotif Channel ready to rcv notif")
        for {
            response, err := stream.Recv()
            if err == io.EOF {
		log.Print("v4: getNotif Stream rcvd EOF.\n")
		errCh <- nil
		return
	    }
	    if err != nil { 
	        errCh <- errors.New("v4: getNotif Stream rcvd error " + err.Error())
		return
            }
	    lck.Lock()
	    jsonResp, _ := json.MarshalIndent(response, "", " ")
	    if response.GetEventType() == pb.SLNotifType_SL_EVENT_TYPE_ROUTE {
                log.Printf("v4: getNotif eventType %v eventJson %v\n", response.GetEventType(), string(jsonResp))
		entries := response.GetRoute().GetEntries()
		for entry:=0;entry<len(entries);entry++ {
                    prefix := entries[entry].GetPrefix()
		    log.Printf("v4: getNotif RouteEntry:%d Prefix %v", entry, int2ip4(prefix)) 
		    pathList := entries[entry].GetPathList()
		    routeCommonPathList(pathList, int2ip4(prefix), entry, 4)
		}
	    } else {
                log.Printf("v4: getNotif eventType %v event %v eventJson %v\n",
		                 response.GetEventType(), response.GetEvent(), string(jsonResp))
	    }
	    lck.Unlock()
	}
    }()
    for _, msg := range msgs {
        if err := stream.Send(msg); err != nil {
            log.Fatalf("v4: getNotif Stream send errored. Exit RPC error: %v\n", err)
            return err
        }
    }
    err = <-errCh
    close(errCh)
    return err
}

func getNotifv6(conn *grpc.ClientConn, ctx context.Context, msgs []*pb.SLRouteGetNotifMsg, wg *sync.WaitGroup, lck *sync.Mutex) error {

    defer wg.Done()

    errCh := make(chan error, 1)

    client := pb.NewSLRoutev6OperClient(conn)
    stream, err := client.SLRoutev6GetNotifStream(ctx)
    if err != nil {
        log.Fatalf("v6: getNotif Could not get stream from client. Exit RPC error  %v", err)
        return err
    }

    go func() {
        log.Print("v6: getNotif Channel ready to rcv notif")
        for {
            response, err := stream.Recv()
            if err == io.EOF {
		log.Print("v6: getNotif Stream rcvd EOF.\n")
                errCh <- nil
		return
            }
	    if err != nil {
                errCh <- errors.New("v6: getNotif Stream rcvd error " + err.Error())
		return
            }
            lck.Lock()
	    jsonResp, _ := json.MarshalIndent(response, "", " ")
            if response.GetEventType() == pb.SLNotifType_SL_EVENT_TYPE_ROUTE {
                log.Printf("v6: getNotif eventType %v: eventJson %v\n", response.GetEventType(), string(jsonResp))
                entries := response.GetRoute().GetEntries()
                for entry:=0;entry<len(entries);entry++{
                    prefix := entries[entry].GetPrefix()
		    log.Printf("v6: getNotif RouteEntry:%d Prefix %v", entry, byte2ip6(prefix))
                    pathList := entries[entry].GetPathList()
                    routeCommonPathList(pathList, prefix, entry, 6)
                    }
            } else {
		    log.Printf("v6: getNotif eventType %v: event %v eventJson %v\n",
		                response.GetEventType(), response.GetEvent(), string(jsonResp))
            }
	    lck.Unlock()
	}
    }()
    for _, msg := range msgs {
        if err := stream.Send(msg); err != nil {
            log.Fatalf("v6: getNotif Stream send errored. Exit RPC error: %v\n", err)
            return err
        }
    }
    err = <-errCh
    close(errCh)
    return err
}

func routeCommonPathList(pathList []*pb.SLRoutePath, prefix net.IP, routeEntry int, afi int) {
    for path:=0;path<len(pathList);path++{
        if afi == 4 {
            nextHop := pathList[path].GetNexthopAddress().GetV4Address()
            if nextHop != 0 {
                log.Printf("v%v RouteEntry:%d Prefix %v Path %d nextHop %v",
                         afi, routeEntry, prefix, path, int2ip4(nextHop))
            }
            remoteAddList := pathList[path].GetRemoteAddress()
            for remoteAdd:=0;remoteAdd<len(remoteAddList);remoteAdd++ {
                 log.Printf("v%v RouteEntry:%d Prefix %v  Path %d remoteAdd %v",
                         afi, routeEntry, prefix, path, int2ip4(remoteAddList[remoteAdd].GetV4Address()))
            }
        } else if afi == 6 {
            nextHop := pathList[path].GetNexthopAddress().GetV6Address()
            if nextHop != nil {
                 log.Printf("v%v RouteEntry:%d Prefix %v Path %d nextHop %v",
                         afi, routeEntry, prefix, path, byte2ip6(nextHop))
            }
            remoteAddList := pathList[path].GetRemoteAddress()
            for remoteAdd:=0;remoteAdd<len(remoteAddList);remoteAdd++{
                log.Printf("v%v RouteEntry:%d Prefix %v  Path %d remoteAdd %v",
                         afi, routeEntry, prefix, path, byte2ip6(remoteAddList[remoteAdd].GetV6Address()))
            }
        }
    }
}
