/*
 * Copyright (c) 2019 by cisco Systems, Inc.
 * All rights reserved.
 */
package sl_api

import (
    "fmt"
    "io"
    "net"
    "strings"
    "time"

    log "github.com/sirupsen/logrus"
    pb "gengo"
    "golang.org/x/net/context"
    "google.golang.org/grpc"
)

var (
    MaxIlmInBatch uint32
)

// runMPLSILMRequestStream sends ILM (incoming label requests) request to router.
func runMPLSILMRequest(conn *grpc.ClientConn, messages []*pb.SLMplsIlmMsg) (err error) {
        client := pb.NewSLMplsOperClient(conn)
        ctx, cancel := context.WithTimeout(context.Background(), 600*time.Second)
        defer cancel() // make sure all paths cancel the context to avoid context leak

        stream, err := client.SLMplsIlmOpStream(ctx)
        if err != nil {
                return err
        }

        errc := make(chan error, 1)
        go func() {
                for {
                        response, err := stream.Recv()
                        if response == nil || err == io.EOF {
                                // read done.
                                close(errc)
                                return
                        }
                        if err != nil {
                                log.Error(err)
                                errc <- err
                                close(errc)
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

func MplsGetMsg(conn *grpc.ClientConn) {

    /* Create a NewSLMplsOperClient instance */
    c := pb.NewSLMplsOperClient(conn)

    /* Create a SLMplsGetMsg */
    mplsGetMsg := &pb.SLMplsGetMsg {}

    /* RPC to Get the mpls values. */
    response, err := c.SLMplsGet(context.Background(), mplsGetMsg)
    if err != nil {
        log.Fatalf("Client Error %v", err)
    }

    /* Print Server response */
    fmt.Println("Max ILMs per batch   : ", response.GetMaxIlmPerIlmmsg())

    MaxIlmInBatch = response.GetMaxIlmPerIlmmsg()
}

func MplsRegOperation(conn *grpc.ClientConn, oper pb.SLRegOp) {

    /* Create a NewSLMplsOperClient instance */
    c := pb.NewSLMplsOperClient(conn)

    /* Create an MPLS registration message */
    message := &pb.SLMplsRegMsg{Oper: oper,}

    /* RPC the Registration message*/
    response, err := c.SLMplsRegOp(context.Background(), message)
    if err != nil {
        log.Fatal(err)
    }

    if response.ErrStatus.Status != pb.SLErrorStatus_SL_SUCCESS {
        log.Fatalf("MPLS registration operation error: ", response.String())
    }
}

func LabelBlockOperation(conn *grpc.ClientConn, oper pb.SLObjectOp,
                         startLabel uint32, numLabels uint32, numElsps uint,
                         clientName string) {

    /* Create a NewSLMplsOperClient instance */
    c := pb.NewSLMplsOperClient(conn)

    /* Label block message */
    message := &pb.SLMplsLabelBlockMsg{Oper: oper,}

    /* Label block type */
    labelBlockType := pb.SLMplsLabelBlockType_SL_MPLS_LABEL_BLOCK_TYPE_SRGB
    if numElsps > 0 {
        labelBlockType = pb.SLMplsLabelBlockType_SL_MPLS_LABEL_BLOCK_TYPE_CBF
    }

    /* Label block key */
    key := &pb.SLMplsLabelBlockKey{
               StartLabel: startLabel,
               LabelBlockSize: numLabels,
               BlockType: labelBlockType,
               ClientName: clientName,
            }

    log.Debug("Label block: start label: ", startLabel, ", #labels: ", numLabels,
              ", block type: ", labelBlockType, ", client name: ", clientName)

    message.MplsBlocks = append(message.MplsBlocks, key)

    /* RPC the message */
    response, err := c.SLMplsLabelBlockOp(context.Background(), message)
    if err != nil {
        log.Fatal(err)
    }

    if response.StatusSummary.Status != pb.SLErrorStatus_SL_SUCCESS {
        log.Fatalf("MPLS label block operation error: ", response.String())
    }
}

/*
 * Given an interface name, e.g, GigabitEthernet0/0/0/x, increment
 * x given the index (idx) and the maxIfIdx which should be the maximum
 * value of x
 *
 * Return the input string unchanged if:
 *   a) There is no "/" in the string
 *   b) idx or maxIfIdx are 0
 *
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

func LabelOperation(conn *grpc.ClientConn, Oper pb.SLObjectOp,
                    startLabel uint, startOutLabel uint, numLabels uint,
                    numPaths uint, numElsps uint, batchNum uint, batchSize uint,
                    NextHopIP string, Interface string, MaxIfIdx uint, AutoIncNHIP bool) {

    var elspIdx, pathIdx, batchIndex uint
    var sentIlms uint = 0
    var totalIlms uint = 0
    var numIlms uint = 0
    var ilmsInBatch uint = 0
    var message *pb.SLMplsIlmMsg = nil
    var cfgElsp bool = false
    var messages []*pb.SLMplsIlmMsg

    if batchSize == 0 {
        log.Fatalf("Invalid batch size: %d", batchSize)
    }

    log.Debug("Label: start label: ", startLabel,
              ", #labels: ", numLabels,
              ", #numPaths: ", numPaths,
              ", #numElsps: ", numElsps,
              ", #batchNum: ", batchNum,
              ", #batchSize: ", batchSize)

    if batchSize > uint(MaxIlmInBatch) {
        batchSize = uint(MaxIlmInBatch)
    }

    /* Initialize some path params */
    nexthop := ip4toInt(net.ParseIP(NextHopIP))

    /* Let's compute the time it takes to RPC the labels */
    t0 := time.Now()

    label := startLabel

    if numElsps > 0 {
        cfgElsp = true
        numIlms = numElsps
    } else {
        numIlms = 1
    }

    totalIlms = numLabels * numIlms
    if batchSize > totalIlms {
        batchSize = totalIlms
    }

    /*
     * numElsps:  > 1 for ELSP, 0 otherwise (configured)
     * totalIlms: numLabels * numElsps (calculated)
     * batchSize: number of ilms per batch (configured)
     * numIlms: number of ilms (1 for non ELSP, numElsps otherwise)
     */
    for sentIlms < totalIlms  {

        log.Debug("sentIlms ", sentIlms,
		  " batchIdx ", batchIndex,
		  " ilmsInBatch ", ilmsInBatch,
		  " numIlms ", numIlms,
		  " batchSize ", batchSize,
		  " sentIlms ", sentIlms,
		  " totalIlms ", totalIlms)

        if (ilmsInBatch + numIlms > batchSize) ||
           (sentIlms + numIlms >= totalIlms)  {
            batchIndex ++

            messages = append(messages, message)

            ilmsInBatch = 0
        }

        if ilmsInBatch == 0  {
            /* Create a new ILM batch */
            message = &pb.SLMplsIlmMsg{Oper: Oper,}
        }

        /* If we are adding ELSP entries then loop and create as many
         * using the same label. If numElsps is set to 0 we just add
         * one ILM entry for that label.
         */

        for elspIdx = 0; elspIdx < numIlms; elspIdx++   {

            log.Debug("label: ", label, " elspIndex: ", elspIdx, " numIlms: ", numIlms)

            nexthopInterface := ifMunge(Interface, elspIdx, MaxIfIdx)
            log.Debug("Interface: ", nexthopInterface)

            var cos *pb.SLMplsCos = nil

            /* Setup some ilm attributes */
            ilm := &pb.SLMplsIlmEntry{
                Key: &pb.SLMplsIlmKey{LocalLabel: uint32(label),},
            }
            if cfgElsp == true {
                if elspIdx <= 7 {
                    cos = &pb.SLMplsCos{Value: &pb.SLMplsCos_Exp{uint32(elspIdx)}}
                } else {
                    cos = &pb.SLMplsCos{Value: &pb.SLMplsCos_DefaultElspPath{true}}
                }
                ilm.Key.SlMplsCosVal = cos
            }

            for pathIdx = 0; pathIdx < numPaths; pathIdx++  {

                nhlfe := &pb.SLMplsPath{
                    VrfName: "default",
                    Action: pb.SlLabelAction_SL_LABEL_ACTION_SWAP,
                    NexthopAddress: &pb.SLIpAddress {
                        Address: &pb.SLIpAddress_V4Address{
                            V4Address: nexthop + uint32(elspIdx),
                        },
                    },
                    NexthopInterface: &pb.SLInterface{
                        Interface: &pb.SLInterface_Name{
                            Name: nexthopInterface,
                        },
                    },
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
                ilm.Paths = append(ilm.Paths, nhlfe)
                if AutoIncNHIP {
                    nexthop = nexthop + 1
                }

            }

            /* Append Route to batch */
            message.MplsIlms = append(message.MplsIlms, ilm)

        }
        sentIlms = sentIlms + numIlms
        ilmsInBatch += numIlms
        label++
    }

    t1 := time.Now()

    fmt.Printf("%s Total Batches: %d, Ilms: %d, Preparation time: %v\n",
        Oper.String(), batchIndex, sentIlms, t1.Sub(t0))

    if (sentIlms > 0) {
        var rate float64
        rate = float64(sentIlms)/(t1.Sub(t0).Seconds())
        fmt.Printf("Preparation Rate: %f\n", rate)
    }

    t0 = time.Now()

    runMPLSILMRequest(conn, messages)

    t1 = time.Now()


    fmt.Printf("%s Total Batches: %d, Ilms: %d, ElapsedTime: %v\n",
        Oper.String(), batchIndex, sentIlms, t1.Sub(t0))

    if (sentIlms > 0) {
        var rate float64
        rate = float64(sentIlms)/(t1.Sub(t0).Seconds())
        fmt.Printf("Programming Rate: %f\n", rate)
    }
}
