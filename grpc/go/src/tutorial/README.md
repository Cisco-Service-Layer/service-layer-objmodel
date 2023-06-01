### GO quick Tutorial

The reader is assumed familiar with the equivalent Python quick start tutorial. This tutorial shows how the same example can be written in GO.

The program can be used to test either the IPv4 or MPLS vertical.

Please refer to <http://golang.org> for more information about GO.

#### Arguments
To get help on running the tutorial:

```
./tutorial -h
```

##### IPv4 Testing

./tutorial [-ipv4]

| Argument | Description |
| --- | --- |
| -ipv4            | Select IPv4 testing (optional, default) |
| -batch_size      | Configure the number of ipv4 routes to be added to a batch |
| -num_batches     | Configure the number of batches |
| -first_prefix    | First prefix to be used (default 20.0.0.0) |
| -prefix_len      | Prefix length to be used in the route operation (default 24) |
| -interface       | Set the name of the next hop interface (default "GigabitEthernet0/0/0/0") |
| -next_hop_ip     | Next Hop IP to be used (default 10.0.0.1) |
| -auto_inc_nhip   | Automatic increament of next hop ip address |
| -route_oper      | Route Operation: Add(1), Update(2), Delete(3) |
| -vrf_reg_oper    | VRF registration Operation: Reg(1), Unregister(2), EOF(3) |

##### MPLS Testing

| Argument | Description |
| --- | --- |
| -mpls        | Select MPLS testing |
| -batch_size   | Configure the number of ILM entries to be added to a batch |
| -start_label | Configure the starting label for this test (default 12000) |
| -start_out_label | Configure the starting out label for this test (default 20000) |
| -num_labels  | Configure the number of labels to be allocated (default 1000) |
| -num_elsps   | Configure the number of ELSP entries to be added for this label (0-9, 0: no-elsp (default), 9: elsp-dflt) |
| -num_paths   | Configure the number of paths to be added per ILM entry (default 1)|
| -interface    | Set the name of the next hop interface (default "GigabitEthernet0/0/0/0") |
| -max_if_idx  | Increment the last index of the interface up to this number based on the number of elsps configured, eg, GE0/0/0/0, GE0/0/0/1, etc |
| -client_name  | The client name to be used during MPLS CBF label block allocation |

#### How to build
If you have a docker environmemt, you can run "make tutorial" from the service-layer-objmodel
top level directory where you see a Dockerfile and a Makefile. This will take some time
the first time but once it completes it should drop you into bash, like so:

```
Bash-Prompt:sl$ make tutorial
```

Once in bash, navigate to the tutorial directory and type "make":
```
root@8e808b09047a:/slapi# cd grpc/go/src/tutorial/
root@8e808b09047a:/slapi/grpc/go/src/tutorial# make
go get github.com/golang/protobuf/proto github.com/sirupsen/logrus golang.org/x/net/context google.golang.org/grpc
go build -o tutorial
```

#### How to run

To run it with default parameters:
./tutorial

#####IPV4 Examples:
1) ./tutorial -ipv4 -interface FourHundredGigE0/0/0/0 -num_batches 5 -batch_size 100 -auto_inc_nhip -route_oper 1 -vrf_reg_oper 1
   Will send: 5 batches of IPV4 routes with 100 routes in each batch with starting prefix: 20.0.0.0/24,
              starting next_hop_ip:10.0.0.1 with interface_name set to FourHundredGigE0/0/0/0.
```
   [20.0.0.0/24, [10.0.0.1, FourHundredGigE0/0/0/0]], [20.0.1.0/24, [10.0.0.2, FourHundredGigE0/0/0/0]], …
```
2) ./tutorial -ipv4 -interface FourHundredGigE0/0/0/0 -num_batches 5 -batch_size 100 -auto_inc_nhip -route_oper 3
   Will send: Delete request of 5 batches of IPV4 routes with 100 routes in each batch with starting prefix: 20.0.0.0/24,
              starting next_hop_ip:10.0.0.1 with interface_name set to FourHundredGigE0/0/0/0.
```
   [20.0.0.0/24, [10.0.0.1, FourHundredGigE0/0/0/0]], [20.0.1.0/24, [10.0.0.2, FourHundredGigE0/0/0/0]], …
```

#####MPLS Examples:
------------

1) ./tutorial -mpls -interface FourHundredGigE0/0/0/0 -start_label 20000 -num_labels 100 -route_oper 1 -vrf_reg_oper 1

   Will send: Add request of 100 ILM routes with starting label 20000 with
              next_hop_ip:10.0.0.1 and interface_name set to FourHundredGigE0/0/0/0.
```
   [20000, [NH1]], [20001, [NH1]], …
```

2) ./tutorial -mpls -interface FourHundredGigE0/0/0/0 -start_label 20000 -num_labels 100 -route_oper 3 -vrf_reg_oper 3

   Will send: Delete request of 100 ILM routes with starting label 20000 with
              next_hop_ip:10.0.0.1 and interface_name set to FourHundredGigE0/0/0/0.
```
   [20000, [NH1]], [20001, [NH1]], …
```

3) ./tutorial -mpls -start_label 30000 -num_labels 1000 -route_oper 1 -vrf_reg_oper 1 -num_elsps 4

   Will send: Add request of 1000 ILM routes with starting label 30000 with EXP0-EXP4 for each label
```
   [30000, EXP0, [NH1]], [30000, EXP1, [NH2]],
   [30001, EXP0, [NH1]], [30001, EXP1, [NH2]],
   …
```
4) ./tutorial -mpls -start_label 30000 -num_labels 1000 -route_oper 3 -vrf_reg_oper 3 -num_elsps 4

   Will send: Delete request of 1000 ILM routes with starting label 30000 with EXP0-EXP4 for each label
```
   [30000, EXP0, [NH1]], [30000, EXP1, [NH2]],
   [30001, EXP0, [NH1]], [30001, EXP1, [NH2]],
   …
```
5) ./tutorial -mpls -start_label 20000 -num_labels 1000 -route_oper 1 -vrf_reg_oper 1 -num_elsps 8 -num_paths 2

   Will send:
```
   [20000, EXP0, [NH1, NH2]], [20000, EXP1, [NH1, NH2]],
       [20000, EXP2, [NH1, NH2]], [20000, EXP3, [NH1, NH2]],,
   [20001, EXP0, [NH1, NH2]], [20001, EXP1, [NH1, NH2]],
       [20001, EXP2, [NH1, NH2]], [20001, EXP3, [NH1, NH2]],,
   …
```
