### C# quick Tutorial
The program Quickstart.cs can be used to test programming of VxLAN tunnel as an Ipv4  route through SLAPI

#### Dependencies
The Quickstart.cs needs dotnet to be installed. Quickstart.csproj has the complete list of dotnet libraries this application depends on.
If dotnet is installed, the dependencies can be resolved by running the following command from this folder
```
dotnet restore
```

#### How to build
From the current folder
```
dotnet build
```
#### Program Invocation
From the current folder, Quickstart can be invoked like given below
```
dotnet run -- -t "172.29.94.88:62704" -d test_vxlan.json
```
Alternatively, using the absolute path to the Quickstart.csproj file we can invoke the application like this
```
dotnet run -p <path>Quickstart.csproj -- -t "172.29.94.88:62704" -d test_vxlan.json
```
Note: The '---' argument is mandatory. It marks the end of arguments to the dotnet runtime and beginning of arguments to the Quickstart application

##### Arguments
From this folder
dotnet run -- --help
| Argument | Description |
| --- | --- |
| - --help       | Show this help text |
| -t <target>    | The target server address in the format <ipv4 address>:<port> |
| -d <path>      | The path to the JSON file having test data compliant with schema test_vxlan_schema.json" |

###### Note
If you don't have dotnet installed, you can do all of the above from inside the docker prompt
launch docker prompt like this
```
make slapi-bash
```
