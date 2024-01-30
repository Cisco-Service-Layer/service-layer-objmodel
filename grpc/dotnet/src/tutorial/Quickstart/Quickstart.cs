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
using System.Net.Http;
using System.Security.Cryptography.X509Certificates;
using Grpc.Net.Client;
using System.IO;
using Google.Protobuf;
using Grpc.Core;
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

    [JsonProperty("authentication_info")]
    public Dictionary<string, object> AuthenticationInfo { get; set; }

    [JsonProperty("certificate_info")]
    public Dictionary<string, object> CertificateInfo { get; set; }

    [JsonProperty("test_flags")]
    public Dictionary<string, object> TestFlags { get; set; }
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
    /// Converts dotted decimal string ipv4 address to unsigned 32 bit integer in network byte order
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

    /// <summary>
    /// Prints ServiceLayer IP Address based on AFI
    /// </summary>
    public static void PrintSlIpAddress(ServiceLayer.SLIpAddress ip)
    {
        switch (ip.AddressCase)  // Adjusted from addressCase_ to AddressCase
        {
            case ServiceLayer.SLIpAddress.AddressOneofCase.V4Address:
                uint ipv4 = ip.V4Address;
                byte[] bytesV4 = BitConverter.GetBytes(ipv4);
                if (BitConverter.IsLittleEndian)
                {
                    Array.Reverse(bytesV4); // Reverse to get the correct byte order
                }
                IPAddress addressV4 = new IPAddress(bytesV4);
                Console.WriteLine(addressV4.ToString());
                break;

            case ServiceLayer.SLIpAddress.AddressOneofCase.V6Address:
                ByteString ipv6Bytes = ip.V6Address;  // Adjusted the type name
                byte[] bytesV6 = ipv6Bytes.ToByteArray();
                IPAddress addressV6 = new IPAddress(bytesV6);  // IPAddress constructor can take byte[] for IPv6
                Console.WriteLine(addressV6.ToString());
                break;

            default:
                Console.WriteLine("Unknown IP type or not set.");
                break;
        }
    }

    /// <summary>
    /// Converts uint32 ipv4 address to dotted decimal string
    /// </summary>
    public static string GetIpv4AddressString(uint ipv4_address)
    {
        byte[] bytesV4 = BitConverter.GetBytes(ipv4_address);
        if (BitConverter.IsLittleEndian)
        {
            Array.Reverse(bytesV4); // Reverse to get the correct byte order
        }
        IPAddress addressV4 = new IPAddress(bytesV4);
        return addressV4.ToString();
    }

    static async Task Main(string[] args)
    {
        TestVxlan testData = null;
        //GrpcChannel channel = null;
        Grpc.Core.Channel channel = null;	
        SLRoutev4Oper.SLRoutev4OperClient client = null;
        SLGlobal.SLGlobalClient kl_client = null;

        SLRoutev4Msg slRoutev4Msg = null;
	var cleanUp = false;
	var autoRegister = false;
	var certType = "no-tls";

        // Process  arguments
        var parsedArgs = ProcessArgs(args);
        var serverIp = parsedArgs.ServerAddress;
        var jsonFilePath = parsedArgs.JsonFilePath;
        string userName = "cisco";
        string passWord = "cisco123";

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
	if (testData.TestFlags != null)
	{
            autoRegister = Convert.ToBoolean(testData.TestFlags["auto_register"]);
            cleanUp = Convert.ToBoolean(testData.TestFlags["clean_up"]);
	}
        if (testData.AuthenticationInfo != null)
        {
            userName = Convert.ToString(testData.AuthenticationInfo["username"]);
            passWord = Convert.ToString(testData.AuthenticationInfo["password"]);
        }

        //Setting exception handling, press ctrl+c to gracefully exit client program
        using var cts = new CancellationTokenSource();
        Console.CancelKeyPress += (s, e) =>
        {
            Console.WriteLine("Cancellation requested.");
            cts.Cancel();
            e.Cancel = true;
        };
        if (testData.CertificateInfo != null)
	{
             certType = Convert.ToString(testData.CertificateInfo["cert_type"]);
        }
        Console.WriteLine("certificate type: " + certType);
        // Setup the channel and client
        if (!string.IsNullOrEmpty(serverIp))
        {
            var serverAddress = $"{serverIp}";
            if (certType == "tls") 
            {
	       string caCertificatePath = Convert.ToString(testData.CertificateInfo["cert_ca_path"]);
	       string chain = File.ReadAllText(caCertificatePath);
	       var certCred = new Grpc.Core.SslCredentials(chain);
               var pswdCred = Grpc.Core.CallCredentials.FromInterceptor((ctx, meta) =>
               {
                   meta.Add("username", userName);
                   meta.Add("password", passWord);
                   return Task.CompletedTask;
               });
               var cred = Grpc.Core.ChannelCredentials.Create(certCred, pswdCred);
               channel = new Grpc.Core.Channel(serverAddress, cred);
            }
            else
            {
                var callCred = Grpc.Core.CallCredentials.FromInterceptor((ctx, meta) =>
                {
                    meta.Add("username", userName);
                    meta.Add("password", passWord);
                    return Task.CompletedTask;
                });
            
                // Use ChannelCredentials.Insecure to create an insecure channel
                channel = new Grpc.Core.Channel(serverAddress, Grpc.Core.ChannelCredentials.Create(Grpc.Core.ChannelCredentials.Insecure, callCred));
            }

            try
            {
                client = new SLRoutev4Oper.SLRoutev4OperClient(channel);
                kl_client = new SLGlobal.SLGlobalClient(channel);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error initializing the client: " + ex.Message);
                Environment.Exit(1);
            }
        }
        else
        {
            Console.WriteLine("Server address is not provided.");
            Environment.Exit(1);
        }

        /* light weight operation that can be periodically called to keep the
         * connection alive
         */
	var slGlobalsGetMsg = new SLGlobalsGetMsg();
        var getGlobalRsp = await kl_client.SLGlobalsGetAsync(slGlobalsGetMsg);
        if (getGlobalRsp.ErrStatus.Status != SLErrorStatus.Types.SLErrno.SlSuccess)
        {
            // The operation was not successful
            Console.WriteLine($"Operation failed with status: {getGlobalRsp.ErrStatus.Status}");
        }
        else
        {
            // The operation was successful,
            Console.WriteLine($"Max VRF Name length: {getGlobalRsp.MaxVrfNameLength}");
            Console.WriteLine($"Max Interface Name Length: {getGlobalRsp.MaxInterfaceNameLength}");
        }


    	if (autoRegister) {
            // Make sure the router is configured with
    	    // grpc service-layer auto-register
            Console.WriteLine("testData.AutoRegister is true, skipping vrf register");
    	}
    	else
    	{
            if (testData.RegisterV4Vrfs != null)
            {
	        if (!cleanUp)
		{
                   // The following line will allow running this
                   // tutorial multiple times without hitting route exists error
		   // in the case where previous run did not do the cleanup
                   await UnRegisterVrfsAsync(client, testData);
		}
                Console.WriteLine("\nTestcase 1: Register Vrfs");
                Console.WriteLine(" Step 1: Get all Vrfs Registered in the server");
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

                // TODO Do mark and sweep of vrfs by
                // a) Un registering vrfs that are no longer needed
                // await UnRegisterVrfsAsync(client, testData);
                // b) Registering vrfs that are not registered yet
                // await RegisterVrfsAsync(client, testData);

                Console.WriteLine(" Step 2: Register new vrfs");
                await RegisterVrfsAsync(client, testData);
                Console.WriteLine(" Step 3: Send Eofs");
                await EofVrfsAsync(client, testData);
            }
            else
            {
                Console.WriteLine("testData.RegisterV4Vrfs is null");
            }
	    }
        if (testData.ProgramV4VxlanRoutes != null)
        {
            Console.WriteLine("\nTestcase 2: Program V4 Routes, Unary");
	        if (autoRegister)
	        {
                //TODO
                //Console.WriteLine("  Step 1: Get all routes in this vrf");
                //await GetRoutesAsync(client, testData.ProgramV4VxlanRoutes["prefix_vrf"].ToString());
                //TODO
                //Mark and sweep of routes in the vrf, add new routes (delta)
                //TODO
                //Console.WriteLine("Step 2: Mark and sweep of routes");
	        }
            Console.WriteLine("  Step 3: Add/Update/Delete routes");
            slRoutev4Msg = new SLRoutev4Msg
            {
                Oper = SLObjectOp.SlObjopAdd, // To ADD new routes
                //Oper = SLObjectOp.SlObjopUpdate, // To MODIFY existing routes
                //Oper = SLObjectOp.SlObjopDelete, // To DELETE existing routes
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
            Console.WriteLine("  Step 4: Verify routes programmed");
            await GetRoutesAsync(client, testData.ProgramV4VxlanRoutes["prefix_vrf"].ToString());
            //Programming the same set of routes again, using streaming RPC
            Console.WriteLine("\nTestcase 3: Programming v4 routes, streaming");
	        // Cleanup previously programmed routes
	        if (autoRegister)
	        {
	            // Delete all the routes that were programmed
		        // Change the Oper to Delete
                slRoutev4Msg.Oper = SLObjectOp.SlObjopDelete;
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
		        // Change Oper back to Add
                slRoutev4Msg.Oper = SLObjectOp.SlObjopAdd;
	        }
	        else
	        {
                // Unregistering to wipe the slate clean before re-programming
                await UnRegisterVrfsAsync(client, testData);
	        }

	        if (!autoRegister)
	        {
                Console.WriteLine(" Step 1: Register Vrfs");
                await RegisterVrfsAsync(client, testData);
                Console.WriteLine(" Step 2: Send Eofs");
                await EofVrfsAsync(client, testData);
	        }

            using (var call = client.SLRoutev4OpStream())
            {
                // Start the response listening task.
                var responseReaderTask = Task.Run(async () =>
                {
                    try
                    {
                        Console.WriteLine(" Step 3: Setup response handler");
                        await foreach (var message in call.ResponseStream.ReadAllAsync())
                        {
                            Console.WriteLine("Streaming response:");
                            Console.WriteLine($"Correlator: {message.Correlator}");
                            Console.WriteLine($"VRF Name: {message.VrfName}");
                            if (message.StatusSummary.Status == SLErrorStatus.Types.SLErrno.SlSuccess)
                            {
                                Console.WriteLine("Error Status: Success");
                            }
                            else if (message.StatusSummary.Status == SLErrorStatus.Types.SLErrno.SlSomeErr)
                            {
                                Console.WriteLine("Error Status: Operation failed for one or more entries");
                                foreach (var result in message.Results)
                                {
                                    if (result.ErrStatus.Status != SLErrorStatus.Types.SLErrno.SlSuccess)
                                    {
                                        Console.WriteLine($"Received error response for route with Prefix {result.Prefix} and error: {result.ErrStatus.Status}");
                                    }
                                }
                            }
                            else
                            {
                                Console.WriteLine($"Error Status: {message.StatusSummary.Status}");
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
                    Console.WriteLine(" Step 4: Programming routes with streaming");
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

	    if (cleanUp)
	    {
            if (autoRegister)
	        {
	            // Delete all the routes that were programmed
                slRoutev4Msg.Oper = SLObjectOp.SlObjopDelete;
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
	        }
	        else
	        {
                // Unregistering to wipe the slate clean before re-programming
                await UnRegisterVrfsAsync(client, testData);
	        }
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
            Console.WriteLine("RegisterVrfsAsync: Success");
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
    /// UnRegisters the vrfs provided in testData into the GRPC Server using handle client
    /// </summary>
    private static async Task UnRegisterVrfsAsync(SLRoutev4Oper.SLRoutev4OperClient client, TestVxlan testData)
    {
        // Create and populate the SLVrfRegMsg for registration.
        var regMsg = new SLVrfRegMsg { Oper = SLRegOp.Unregister };
        JArray vrfJArray = (JArray)testData.RegisterV4Vrfs["vrf_list"];
        List<string> vrfList = vrfJArray.ToObject<List<string>>();

        foreach (string vrfName in vrfList)
        {
            regMsg.VrfRegMsgs.Add(new SLVrfReg
            {
                VrfName = vrfName,
            });
        }

        // Call the SLRoutev4VrfRegOp RPC
        var regResponse = await client.SLRoutev4VrfRegOpAsync(regMsg);
        if (regResponse.StatusSummary.Status == SLErrorStatus.Types.SLErrno.SlSuccess)
        {
            Console.WriteLine("UnRegisterVrfsAsync:  Success");
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
    /// Send EOF for given vrf
    /// </summary>
    private static async Task EofVrfsAsync(SLRoutev4Oper.SLRoutev4OperClient client, TestVxlan testData)
    {
        // Create and populate the SLVrfRegMsg for EOF operation.
        var eofMsg = new SLVrfRegMsg { Oper = SLRegOp.Eof };
        JArray vrfJArray = (JArray)testData.RegisterV4Vrfs["vrf_list"];
        List<string> vrfList = vrfJArray.ToObject<List<string>>();

        foreach (string vrfName in vrfList)
        {
            eofMsg.VrfRegMsgs.Add(new SLVrfReg
            {
                VrfName = vrfName,
            });
        }

        // Call the SLRoutev4VrfRegOp RPC
        var eofResponse = await client.SLRoutev4VrfRegOpAsync(eofMsg);
        if (eofResponse.StatusSummary.Status == SLErrorStatus.Types.SLErrno.SlSuccess)
        {
            Console.WriteLine("EofVrfsAsync: Success");
        }
        else if (eofResponse.StatusSummary.Status == SLErrorStatus.Types.SLErrno.SlSomeErr)
        {
            Console.WriteLine("Operation failed for one or more entries");
            foreach (var result in eofResponse.Results)
            {
                if (result.ErrStatus.Status != SLErrorStatus.Types.SLErrno.SlSuccess)
                {
                    Console.WriteLine($"Operation failed for VRF Name: {result.VrfName} with error: {result.ErrStatus.Status}");
                }
            }
        }
        else
        {
            Console.WriteLine($"Operation failed with error: {eofResponse.StatusSummary.Status}");
        }
    }

    private static SLRoutev4GetMsg PrintRouteResponse(SLRoutev4GetMsgRsp getRouteResponse)
    {
	var markerRoute = new SLRoutev4GetMsg();
        // Print the response correlator, EOF status, and VRF name
        Console.WriteLine($"Response Correlator: {getRouteResponse.Correlator}");
        Console.WriteLine($"EOF Status: {getRouteResponse.Eof}");
        Console.WriteLine($"VRF Name: {getRouteResponse.VrfName}");

	markerRoute.EntriesCount = 1;
	markerRoute.VrfName = getRouteResponse.VrfName;
	markerRoute.GetNext = !getRouteResponse.Eof;

        // If successful, iterate through the returned IPv4 routes
        foreach (var route in getRouteResponse.Entries)
        {
            Console.WriteLine($"------------------------------------");
            Console.WriteLine($"IPv4 Prefix: {GetIpv4AddressString(route.Prefix)}");
            Console.WriteLine($"IPv4 Prefix Length: {route.PrefixLen}");
	    markerRoute.Prefix = route.Prefix;
	    markerRoute.PrefixLen = route.PrefixLen;

            // For each route, iterate through its path list
            foreach (var path in route.PathList)
            {
                Console.WriteLine($"    Path VRF Name: {path.VrfName}");
                Console.WriteLine($"    Encapsulation Type: {path.EncapType}");

                // If the path has a VxLAN encapsulation, print its details
                if (path.EncapType == SLEncapType.SlEncapVxlan)
                {
                    var vxlan = path.VxLANPath;
                    Console.WriteLine($"        VNI: {vxlan.VNI}");

                    // Convert bytes to MAC addresses (assuming standard MAC format)
                    Console.WriteLine($"        Source MAC Address: {BitConverter.ToString(vxlan.SourceMacAddress.ToByteArray()).Replace("-",":")}");
                    Console.WriteLine($"        Destination MAC Address: {BitConverter.ToString(vxlan.DestMacAddress.ToByteArray()).Replace("-",":")}");
                    Console.Write($"        Source IP Address: ");
                    PrintSlIpAddress(vxlan.SrcIpAddress);
                    Console.Write($"        Destination IP Address: ");
                    PrintSlIpAddress(vxlan.DestIpAddress);
                }
            }
        }
	return markerRoute;
    } 
    private static async Task GetRoutesAsync(SLRoutev4Oper.SLRoutev4OperClient client, string vrf_name)
    {
        // Create and populate the SLRoutev4GetMsg.
        var markerRouteMsg = new SLRoutev4GetMsg
        {
            VrfName = vrf_name,
            //Prefix = 0xAC101E00,
            //PrefixLen = 24,
            EntriesCount = 10,   // Fetch n  entries upto 1000 entries at once
            GetNext = false     // GetNext set to false in the case we are trying to get the first set and there is no marker 
        };

	do 
	{
            // Call the SLRoutev4Get RPC
            var getRouteResponse = await client.SLRoutev4GetAsync(markerRouteMsg);
            if (getRouteResponse.ErrStatus.Status != SLErrorStatus.Types.SLErrno.SlSuccess)
            {
                // The operation was not successful
                Console.WriteLine($"Operation failed with status: {getRouteResponse.ErrStatus.Status}");
            }
            else
            {
                //Print the response
                markerRouteMsg = PrintRouteResponse(getRouteResponse);

            }
	} while (markerRouteMsg.GetNext);
    }
}
