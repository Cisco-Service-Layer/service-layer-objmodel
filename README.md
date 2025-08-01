# Service Layer API

## Introduction

In IOS-XR, routing protocols make use of services provided by the Routing Information Base (RIB), the MPLS label manager, BFD, and other modules, in order to program the forwarding plane. Such programming is exposed through the service layer API, which is very rich in nature.

Exposing the Service Layer API as a Google RPC (or GRPC), over Google protocol buffers (Protobuf or GPB), enables customers to write their own applications, routing protocols, controllers, etc., whether on box or off box, in a rich set of languages including C++, Python, GO, etc.

## Getting Started

Clone or checkout the branch corresponding to your IOS-XR release. For example:
```
git clone https://github.com/Cisco-Service-Layer/service-layer-objmodel.git -b 6.6.3
```
or if you have already cloned
```
git checkout 6.6.3
```

## Service Layer Verticals

The Service Layer API is currently organized in a set of files that expose certain verticals e.g. IPv4 RIB functionality, or MPLS functionality, etc.
In the initial releases, the focus is to provide the following verticals:

* Initialization: This optional RPC sets up a heartbeat channel based on GRPC streaming mechanism. It can also be used to determine the API version implemented by the server.
* IPv4, IPv6 Route: This mainly handles any IPv4 or IPv6 route additions into the node based on a certain VRF.
* MPLS Incoming Label Maps (ILMs): This mainly handles any incoming MPLS label mapping to a forwarding function.
* IPv4, IPv6 BFD: This mainly handles managing BFD sessions, and getting corresponding BFD session state notifications.
* Interfaces: This mainly allows registered clients to get interface state event notifications.
* L2: This mainly handles L2 route changes and Bridge-Domain (BD) registrations. 
* AF: This vertical provides a simplified set of RPCs to program IPv4 Route, IPv6 Route, MPLS Incoming Label Maps and PathGroups. The RPC also supports advanced features such as reprogramming on viability change, and FIB acknowledgement for programming operations.
* More functions may be added in the future.

### Vertical RPC functions

Each function vertical, e.g. RIB vertical, declares a "template" set of RPCs that is more or less consistently followed throughout other verticals. Some of these template RPCs are explained here:

* **(Vertical)Get()**: This is mainly used to query certain capabilities for that vertical.
* **(Vertical)GetStats()**: This is mainly used to query vertical specific statistics.
* **(Vertical)RegOp()**: This is mainly used to Register/Unregister/EoF, which basically notifies the service layer server about interest in the vertical, no interest, and end of file (EoF), respectively. The EoF marker is especially useful on replay of objects in certain restart scenarios.
* **(Vertical)(Object)Op()**: This is mainly used to add, delete, update objects. The convention used for add and update, is that, object 'adds' may fail if the object already exists, whereas update can create or simply override the object if it exists.
* **(Vertical)(Object)Get()**: This is mainly used to retrieve an object or a set of objects.
* **Stream()**: This is mainly a GRPC "streaming" version of the non-streaming version of the function.
* **Notif()**: This is mainly a streaming notification function, e.g. asynchronous BFD session state events' streaming.

The Service Layer API allows for GRPC unary functions in most cases, and GRPC streaming in other cases. The former can be rendered in both synchronous and asynchronous modes (depends on the language). The latter is used for continuous transmitting and/or receiving of objects in an asynchronous fashion. This is especially useful to boost performance in certain cases. Please refer to the GRPC website for more information: <http://grpc.io>
In addition, certain RPCs may also allow for batching e.g. creating a number of routes in a single RPC call (in a batch).

Each RPC usually takes a GRPC "message" or request, typically labeled (Something)Msg, example SLRoutev4Msg, which defines the parameters of the request, and return another "message", typically labeled (Something)MsgRsp as a response to the RPC request, example SLRoutev4MsgRsp.

## Documentation

Note that all files are annotated with detailed documentation.
The user of the API can use Doxygen to render his/her own local documentation, refer to instructions under docs directory. The html generated documentation is broken up into sections that describe the messages, verticals, files, etc, and are very useful for quick reference.

## SL API Version
The SL API version is stored in the file grpc/protos/sl_version.proto. Comprised of a major version, minor version, and subversion.  Represents the current version of SL-API as defined by the proto files.

| API Version   | Feature Set |
| ------------- | ------------- |
| 0.1.0  | Routing, MPLS, Interface and BFD RPCs  |
| 0.2.0  | L2RIB RPCs |
| 0.3.0  | MPLS Class Based Forwarding |
| 0.6.0  | Service-Layer and SR merge, Primary/backup (aka Path Priority) for MPLS CBF, Route download priority |
| 0.7.0  | VxLAN encapsulation for IP routes |
| 0.9.0  | Service-Layer AF common RPCs |

## Release Branches

You must checkout the branch corresponding to your IOS-XR release. This branch will contain:
- The proto files with the correct SL API Version for that IOS-XR release
- A Dockerfile with the correct toolchain versions.
- Generated bindings for Python, Golang, C++ and DotNet.

These bindings have been generated using the same toolchain versions as the gRPC server running on the corresponding IOS-XR release. You may directly use these bindings or generate them yourself.

The bindings can be generated within a docker container created by the service layer top makefile. This may take some time the first time.
```
# cd (top level)
# make bindings (creates/launches container and generates bindings)

Note, if needed, setup the proxy variables within ./Dockerfile (just after FROM):
ENV FTP_PROXY="http://proxy:80"
ENV HTTPS_PROXY="http://proxy:80"
ENV HTTP_PROXY="http://proxy:80"
ENV https_proxy="http://proxy:80"
ENV http_proxy="http://proxy:80"
```

The bindings will be generated in the following directories:
```
grpc/go/src/gengo
grpc/python/src/genpy
grpc/cpp/src/gencpp
grpc/dotnet/src/gencs
```
The bindings can also be generated manually using protoc in an environment with the correct toolchain versions. The toolchain versions in the Dockerfile:
* GO_VER: Go version
* GRPC_VER: gRPC version
* PROTOBUF_VER: libprotoc version
* GO_PROTOBUF_VER: protoc-gen-go version
* GENPROTO_VER: go-genproto version

# Checking Out Tags
In most cases a branch can be checked out directly, but in some cases it may be requested that you checkout a tag instead.

```
git checkout <tag>
```

The tags are named
```
<xr-release>/<sl-api-version>_<revision>

Eg. 6.6.3/v1.2.3_1
```

or,

# Checking Out Commit Hashes
If required the hash at which the gRPC server bindings were comitted to Github can be retrieved by running the following command on a router.
```
# On router
RP/0/RP0/CPU0#show service-layer grpc-proto-hash
Tue Dec 10 13:36:53.522 PST
84c0190a3e09d2183ef3e56b60512f030a54b402
```
And then checkout that commit hash
```
git checkout 84c0190a3e09d2183ef3e56b60512f030a54b402
```

## Tutorials

Finally, please note that the API comes with the following tutorials:

### Python

A quick start tutorial written in Python. The intent here is to get the user a jump-start on hooking up with the API. The reader is advised to try this next.

It can be found here:
```
 grpc/python/src/tutorial/
```

Please check the tutorial [README](/grpc/python/src/tutorial/README.md) for instructions on how to setup the server and python enviromnent.

### Golang (Go)

Another similar tutorial written in GO (golang). This tutorial's code is pre-compiled and committed in the code repo for a quick start on some of the API key features showing batching, etc.

It can be found here:

```
grpc/go/src/tutorial/quickstart.go
```
The executable can be found here:
```
grpc/go/src/tutorial/tutorial
```

A makefile exists in the tutorial directory and could be invoked to re-build the tutorial. To build:

```
# cd (top level)
# make tutorial (creates/launches container)
```

### Cpp

Another similar tutorial written in Cpp (C++) [README](grpc/cpp/src/tutorial/rshuttle/README.md). The tutorial's code is pre-compiled and commited in the code repo for a quick start.

More information on it can be found in:

```
grpc/cpp/src/tutorial/rshuttle
```

### Dotnet (C#)

Another similar tutorial written in Dotnet (C#). This tutorial's code is pre-compiled and committed in the code repo for a quick start on some of the API key features showing batching, etc.

The C# project can be found here:

```
grpc/dotnet/src/tutorial/Quickstart/quickstart.csproj
```
Please refer  README file in Quickstart directory for information on rebuild and running the Quickstart

We can generate documentation for dotnet proto bindings invoking make dotnet-docs
```
# cd (top level)
# make dotnet-docs
```
This will generate html documentation in grpc/dotnet/docs/html/



## Summary

We hope that the above was useful quick overview about the Service Layer API. We recommend that the reader go over the Python quick tutorial first and then go over the .proto files under grpc/protos (or look at the generated .html pages - these are not kept in this repo, but can be auto-generated from this repo).

## Notes

In proto3, if the message field is implicit, and it is set to its default value, proto3 will not serialize this field and it will be omitted from the message payload. This is standard behavior due to the proto3 serialization rules and does not require any special handling in client applications. For more information, see the official documentation: <https://protobuf.dev/programming-guides/proto3/>

For example, in the context of `SLAFGetMsgRsp` [grpc/protos/sl_af.proto](grpc/protos/sl_af.proto), if the `ClientID` field is set to 0, the `ClientID` field will not appear in the serialized response message. For any other client ID value, the field will be included in the response.

Please note, this is a feature of the underlying technology (gRPC/proto3) and not specific to the SL-API. This note is included for clarity.
