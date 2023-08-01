### C# quick Tutorial
The program Quickstart.cs can be used to test programming of VxLAN tunnel as an Ipv4  route

#### Dependencies
The Quickstart.cs needs dotnet to be installed. Quickstart.csproj file constains the dependencies
If dotnet is installed, the dependencies can be resolved by running 'dotnet restore' from this folder

#### How to build
From the current folder
```
dotnet build
```
#### Program Invocation
From the root folder of the repository, Quickstart can be invoked like given below

```
dotnet run -p grpc/dotnet/src/tutorial/Quickstart/Quickstart.csproj -- --help
```
##### Arguments
From this folder
dotnet run -- --help
| Argument | Description |
| --- | --- |
| -t <target>    | The target server address in the format <ipv4 address>:<port> |
| -d <path>      | The path to the JSON file having test data compliant with schema test_vxlan_schema.json" |

###### Note
If you don't have dotnet installed, you can do all of the above from inside the docker prompt
launch docker prompt like this
```
make slapi-bash
```
