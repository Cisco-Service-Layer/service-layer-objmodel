/*
 * Copyright (c) 2023 by cisco Systems, Inc.
 * All rights reserved.
 */
using System;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.IO;
using Google.Protobuf;
using Grpc.Core;
using Grpc.Net.Client;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using Newtonsoft.Json.Linq;
using ServiceLayer;
/// <summary>
/// Defines the primary keys from json data file
/// </summary>
public class TestVxlan
{
    [JsonProperty("register_v4_vrfs")]
    public Dictionary<string, object> RegisterV4Vrfs { get; set; }

    [JsonProperty("program_v4_vxlan_routes")]
    public Dictionary<string, object> ProgramV4VxlanRoutes { get; set; }
}

/// <summary>
/// Defines the arguments parsed from commandline
/// </summary>
public class ParsedArguments
{
    public string ServerAddress { get; set; }
    public string JsonFilePath { get; set; }
}

/// <summary>
/// Implements GRPC client that exercises the SLAPI RPCs for IPv4 Vertical
/// defined in
/// https://github.com/Cisco-Service-Layer/service-layer-objmodel/blob/master/grpc/protos/sl_route_ipv4.proto
/// This implementation particularly exercises L3 VxLAN tunnels
/// </summary>
class SLClient
{
    /// <summary>
    /// Coverts dotted decimal string ipv4 address to unsigned 32 bit integer in network byte order
    /// </summary>
    public static uint IpToUInt32(string ipString)
    {
        var ipAddress = IPAddress.Parse(ipString);
        var bytes = ipAddress.GetAddressBytes();

        if (BitConverter.IsLittleEndian)
        {
            Array.Reverse(bytes);
        }

        return BitConverter.ToUInt32(bytes, 0);
    }
    /// <summary>
    /// Converts Ipv6 Address string to byte string
    /// </summary>
    public static ByteString GetIPv6ByteString(string ipv6String)
    {
        IPAddress ipAddress = IPAddress.Parse(ipv6String);
        byte[] ipBytes = ipAddress.GetAddressBytes();
        return ByteString.CopyFrom(ipBytes);
    }
    /// <summary>
    /// Converts MAC Address string to byte string
    /// </summary>
    public static ByteString MACStringToByteString(string mac)
    {
        byte[] macBytes = mac.Split(':')
                             .Select(x => Convert.ToByte(x, 16))
                             .ToArray();
        return ByteString.CopyFrom(macBytes);

    }

    static async Task Main(string[] args)
    {
        TestVxlan testData = null;
        GrpcChannel channel = null;
        SLRoutev4Oper.SLRoutev4OperClient client = null;

        // Process  arguments
        var parsedArgs = ProcessArgs(args);
        var serverAddress = parsedArgs.ServerAddress;
        var jsonFilePath = parsedArgs.JsonFilePath;

        if (!string.IsNullOrEmpty(jsonFilePath))
        {
            try
            {
                var jsonString = File.ReadAllText(jsonFilePath);
                //Console.WriteLine($"Read JSON: {jsonString}");

                var settings = new JsonSerializerSettings
                {
                    ContractResolver = new DefaultContractResolver
                    {
                        NamingStrategy = new SnakeCaseNamingStrategy()
                    }
                };
                testData = JsonConvert.DeserializeObject<TestVxlan>(jsonString, settings);

                if (testData == null)
                {
                    Console.WriteLine("Deserialization resulted in null object. Check your JSON structure.");
                    Environment.Exit(1);
                }
                else
                {
                    //Console.WriteLine($"Deserialized to object: {JsonConvert.SerializeObject(testData)}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
                Environment.Exit(1);
            }
        }
        else
        {
            Console.WriteLine("JSON file path is not provided.");
            Environment.Exit(1);
        }

        // Setup the channel and client
        if (!string.IsNullOrEmpty(serverAddress))
        {
            AppContext.SetSwitch("System.Net.Http.SocketsHttpHandler.Http2UnencryptedSupport", true);

            channel = GrpcChannel.ForAddress($"http://{serverAddress}",
                                             new GrpcChannelOptions { Credentials = ChannelCredentials.Insecure });

            try {
                client = new SLRoutev4Oper.SLRoutev4OperClient(channel);
            } catch (Exception ex) {
                Console.WriteLine("Error initializing the client: " + ex.Message);
                Environment.Exit(1);
            }
        }
        else
        {
            Console.WriteLine("Server address is not provided.");
            Environment.Exit(1);
        }
        if (testData.RegisterV4Vrfs != null)
        {
            await RegisterVrfsAsync(client, testData);
            // Create and populate the SLVrfRegGetMsg.
            var getMsg = new SLVrfRegGetMsg
            {
                EntriesCount = 10,
                GetNext = true
            };

            // Call the SLRoutev4VrfRegGet RPC
            var getResponse = await client.SLRoutev4VrfRegGetAsync(getMsg);
            if (getResponse.ErrStatus.Status != SLErrorStatus.Types.SLErrno.SlSuccess)
            {
                // The operation was not successful
                Console.WriteLine($"Operation failed with status: {getResponse.ErrStatus.Status}");
            }
            else
            {
                // The operation was successful, so print the SLVrfReg entries
                foreach (var entry in getResponse.Entries)
                {
                    Console.WriteLine($"VRF Name: {entry.VrfName}");
                    Console.WriteLine($"Admin Distance: {entry.AdminDistance}");
                    Console.WriteLine($"VRF Purge Interval Seconds: {entry.VrfPurgeIntervalSeconds}");
                    Console.WriteLine();  // newline for better formatting
                }
            }
        }
        else
        {
            Console.WriteLine("testData.RegisterV4Vrfs is null");
        }
        if (testData.ProgramV4VxlanRoutes != null)
        {
            //var batchSize = Convert.ToInt32(testData.ProgramV4VxlanRoutes["batch_size"]);
            var slRoutev4Msg = new SLRoutev4Msg
            {
                Oper = SLObjectOp.SlObjopAdd,
                Correlator = 1,
                VrfName = testData.ProgramV4VxlanRoutes["prefix_vrf"].ToString(),
            };
            var routesData = testData.ProgramV4VxlanRoutes["route_list"] as JArray;
            foreach (JObject route in routesData)
            {
                var slRoutev4 = new SLRoutev4
                {
                    Prefix = IpToUInt32(route["prefix"].ToString()),
                    PrefixLen = Convert.ToUInt32(route["prefix_len"]),
                };
                var pathsData = route["path_list"] as JArray;
                foreach (JObject path in pathsData)
                {
                    var slRoutePath = new SLRoutePath
                    {
                                VrfName = path["path_vrf"].ToString(),
                        Flags = (bool)path["single_path"] ? 0x00000001U : 0x00000000U
                    };
                    if (path["encap_type"].ToString() == "encap_vxlan")
                    {
                        slRoutePath.EncapType = SLEncapType.SlEncapVxlan;
                        slRoutePath.VxLANPath = new SLVxLANPath
                        {
                            VNI = Convert.ToUInt32(path["vni"]),
                            SourceMacAddress = MACStringToByteString(path["vxlan_src_mac"].ToString()),
                            DestMacAddress = MACStringToByteString(path["vxlan_dst_mac"].ToString())
                        };
                        var encapAfi = Convert.ToInt32(path["encap_afi"]);
                        if (encapAfi == 4)
                        {
                            slRoutePath.VxLANPath.SrcIpAddress = new SLIpAddress
                            {
                                V4Address = IpToUInt32(path["v4_src_ip"].ToString())
                            };
                            slRoutePath.VxLANPath.DestIpAddress = new SLIpAddress
                            {
                                V4Address = IpToUInt32(path["v4_dst_ip"].ToString())
                            };
                        }
                        else if (encapAfi == 6)
                        {
                            slRoutePath.VxLANPath.SrcIpAddress = new SLIpAddress
                            {
                                V6Address = GetIPv6ByteString(path["v6_src_ip"].ToString())
                            };
                            slRoutePath.VxLANPath.DestIpAddress = new SLIpAddress
                            {
                                V6Address = GetIPv6ByteString(path["v6_dst_ip"].ToString())
                            };
                        }
                    }
                    // Add each constructed path to the PathList of slRoutev4
                    slRoutev4.PathList.Add(slRoutePath);
                    if ((bool)path["single_path"])
                    {
                        break;
                    }
                }
                slRoutev4Msg.Routes.Add(slRoutev4);
            }
            try {
                // Make the RPC call
                var response = client.SLRoutev4Op(slRoutev4Msg);

                // Process the response
                Console.WriteLine("Response Correlator: " + response.Correlator);
                Console.WriteLine("Response VRF name: " + response.VrfName);

                // Process status
                var statusSummary = response.StatusSummary.Status;
                Console.WriteLine("Response Status Summary: " + statusSummary);

                // Process results
                foreach (var result in response.Results) {
                    Console.WriteLine("Route error status: " + result.ErrStatus.Status);
                    Console.WriteLine("Route prefix: " + result.Prefix);
                    Console.WriteLine("Route prefix length: " + result.PrefixLen);
                }
            } catch (RpcException e) {
                // RPC failed
                Console.WriteLine("RPC failed: " + e.Status.Detail);
            } catch (Exception ex) {
                // Other exceptions
                Console.WriteLine("Operation failed: " + ex.Message);
            }
            //press ctrl+c to gracefully exit client program
            using var cts = new CancellationTokenSource();
            Console.CancelKeyPress += (s, e) =>
            {
                Console.WriteLine("Cancellation requested.");
                cts.Cancel();
                e.Cancel = true;
            };
            //Programming the same set of routes again, using streaming RPC
            //Send EOF and re-register vrfs to reset the server state so
            //that re-programming the same routes will not return
            //route exists error
            await EofVrfsAsync(client);
            await RegisterVrfsAsync(client, testData);
            using (var call = client.SLRoutev4OpStream())
            {
                // Start the response listening task.
                var responseReaderTask = Task.Run(async () =>
                {
                    try
                    {
                        await foreach (var message in call.ResponseStream.ReadAllAsync())
                        {
                            Console.WriteLine($"Correlator: {message.Correlator}");
                            Console.WriteLine($"VRF Name: {message.VrfName}");
                            Console.WriteLine($"Error Status: {message.StatusSummary}");
                            foreach (var result in message.Results)
                            {
                                IPAddress ipAddr = new IPAddress(BitConverter.GetBytes(result.Prefix).Reverse().ToArray());
                                Console.WriteLine($"Received error response for route with Prefix {ipAddr} and PrefixLen {result.PrefixLen}");
                            }
                        }
                    }
                    catch (RpcException ex)
                    {
                        Console.WriteLine($"An RPC error occurred: {ex.Status.Detail}");
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"An unexpected error occurred: {ex.Message}");
                    }
                }, cts.Token);

                try
                {
                    // Writing messages to the server.
                    await call.RequestStream.WriteAsync(slRoutev4Msg);
                    // When all messages are written, we signal the server by completing our writing side of the stream.
                    await call.RequestStream.CompleteAsync();
                    await responseReaderTask;
                }
                catch (RpcException ex)
                {
                    Console.WriteLine($"An RPC error occurred: {ex.Status.Detail}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"An unexpected error occurred: {ex.Message}");
                }
            }
        }
        else
        {
            Console.WriteLine("testData.ProgramV4VxlanRoutes is null");
        }
        await channel.ShutdownAsync();
    }
    /// <summary>
    /// Parse command line arguments 
    /// </summary>
    private static ParsedArguments ProcessArgs(string[] args)
    {
        var parsedArgs = new ParsedArguments();

        for (int i = 0; i < args.Length; i++)
        {
            switch (args[i])
            {
                case "-h":
                case "--help":
                    ShowHelp();
                    Environment.Exit(0);
                    break;
                case "-t":
                    parsedArgs.ServerAddress = GetNextArgument(i++, args, "-t  incomplete argument check --help");
                    break;
                case "-d":
                    parsedArgs.JsonFilePath = GetNextArgument(i++, args, "-d incomplete argument check --help");
                    break;
                default:
                    Console.WriteLine("Unknown option: " + args[i] + "\nUse -h or --help to display the help text.");
                    Environment.Exit(1);
                    break;
            }
        }

        return parsedArgs;
    }
    /// <summary>
    /// Utility function to get the next command line argument
    /// </summary>
    private static string GetNextArgument(int i, string[] args, string errorMessage)
    {
        if (i + 1 < args.Length) // Check if there is another argument following the current one
        {
            return args[i + 1];
        }
        else
        {
            Console.WriteLine(errorMessage);
            Environment.Exit(1);
            return null; // To satisfy the function's return type
        }
    }
    /// <summary>
    /// Prints help for command line arguments
    /// </summary>
    private static void ShowHelp()
    {
        Console.WriteLine("Usage: Quickstart [options]\n" +
                          "\nOptions:\n" +
                          "  -h, --help      Show this help text.\n" +
                          "  -t <target>     The target server address in the format \"<ipv4 address>:<port>\".\n" +
                          "  -d <path>       The path to the JSON file having test data compliant with schema test_vxlan_schema.json");
    }
    /// <summary>
    /// Registers the vrfs provided in testData into the GRPC Server using handle client
    /// </summary>
    private static async Task RegisterVrfsAsync(SLRoutev4Oper.SLRoutev4OperClient client, TestVxlan testData)
    {
        // Create and populate the SLVrfRegMsg for registration.
        var regMsg = new SLVrfRegMsg { Oper = SLRegOp.Register };
        int purgeInterval = Convert.ToInt32(testData.RegisterV4Vrfs["purge_interval"]);
        int adminDistance = Convert.ToInt32(testData.RegisterV4Vrfs["admin_distance"]);
        JArray vrfJArray = (JArray)testData.RegisterV4Vrfs["vrf_list"];
        List<string> vrfList = vrfJArray.ToObject<List<string>>();

        foreach (string vrfName in vrfList)
        {
            regMsg.VrfRegMsgs.Add(new SLVrfReg
            {
                VrfName = vrfName,
                AdminDistance = (uint)adminDistance,
                VrfPurgeIntervalSeconds = (uint)purgeInterval
            });
        }

        // Call the SLRoutev4VrfRegOp RPC
        var regResponse = await client.SLRoutev4VrfRegOpAsync(regMsg);
        if (regResponse.StatusSummary.Status == SLErrorStatus.Types.SLErrno.SlSuccess)
        {
            Console.WriteLine("Operation was successful");
        }
        else if (regResponse.StatusSummary.Status == SLErrorStatus.Types.SLErrno.SlSomeErr)
        {
            Console.WriteLine("Operation failed for one or more entries");
            foreach (var result in regResponse.Results)
            {
                if (result.ErrStatus.Status != SLErrorStatus.Types.SLErrno.SlSuccess)
                {
                    Console.WriteLine($"Operation failed for VRF Name: {result.VrfName} with error: {result.ErrStatus.Status}");
                }
            }
        }
        else
        {
            Console.WriteLine($"Operation failed with error: {regResponse.StatusSummary.Status}");
        }
    }
    /// <summary>
    /// Send EOF to all vrfs marking end of programming
    /// </summary>
    private static async Task EofVrfsAsync(SLRoutev4Oper.SLRoutev4OperClient client)
    {
        // Create and populate the SLVrfRegMsg for EOF operation.
        var eofMsg = new SLVrfRegMsg
        {
            Oper = SLRegOp.Eof
        };

        // Call the SLRoutev4VrfRegOp RPC
        var eofResponse = await client.SLRoutev4VrfRegOpAsync(eofMsg);
        if (eofResponse.StatusSummary.Status != SLErrorStatus.Types.SLErrno.SlSuccess)
        {
            Console.WriteLine($"Operation failed with error: {eofResponse.StatusSummary.Status}");
        }
    }
}
