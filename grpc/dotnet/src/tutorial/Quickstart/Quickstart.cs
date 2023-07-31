using System;
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

public class TestVxlan
{
    [JsonProperty("register_v4_vrfs")]
    public Dictionary<string, object> RegisterV4Vrfs { get; set; }

    [JsonProperty("register_v6_vrfs")]
    public Dictionary<string, object> RegisterV6Vrfs { get; set; }

    [JsonProperty("program_v4_vxlan_routes")]
    public Dictionary<string, object> ProgramV4VxlanRoutes { get; set; }
}

class SLClient
{
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

    public static ByteString GetIPv6ByteString(string ipv6String)
    {
        IPAddress ipAddress = IPAddress.Parse(ipv6String);
        byte[] ipBytes = ipAddress.GetAddressBytes();
        return ByteString.CopyFrom(ipBytes);
    }

    public static ByteString MACStringToByteString(string mac)
    {
        byte[] macBytes = mac.Split(':')
                             .Select(x => Convert.ToByte(x, 16))
                             .ToArray();
        
        return ByteString.CopyFrom(macBytes);
    }

    static async Task Main(string[] args)
    {
        string serverAddress = string.Empty;
        string jsonFilePath = string.Empty;
        TestVxlan testData = null;
        GrpcChannel channel;
        SLRoutev4Oper.SLRoutev4OperClient client = null;

        // Iterate over the arguments
        for(int i = 0; i < args.Length; i++)
        {
            switch(args[i])
            {
                case "-h":
                case "--help":
                    Console.WriteLine("This is help text for the application.");
                    break;
                case "-t":
                    if (i + 1 < args.Length) // Check if there is another argument following "-t"
                    {
                        Console.WriteLine("The value provided for -t is: " + args[i + 1]);
                        serverAddress = args[i + 1];
                        i++; // Skip the next iteration since we've already processed the following argument
                    }
                    else
                    {
                        Console.WriteLine("The -t option requires a following argument");
	                Environment.Exit(1);
                    }
                    break;
                case "-d":
                    if (i + 1 < args.Length) // Check if there is another argument following "-d"
                    {
                        jsonFilePath = args[i + 1];
                        i++; // Skip the next iteration since we've already processed the following argument
                    }
                    else
                    {
                        Console.WriteLine("The -d option requires a following argument");
	                Environment.Exit(1);
                    }
                    break;
                default:
                    Console.WriteLine("Unknown option: " + args[i]);
	            Environment.Exit(1);
		    break;
            }
        }

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
            
            var routesData = testData.ProgramV4VxlanRoutes["routes"] as JArray;
            foreach (JObject route in routesData)
            {
                var slRoutev4 = new SLRoutev4
                {
                    Prefix = IpToUInt32(route["prefix"].ToString()),
                    PrefixLen = Convert.ToUInt32(route["prefix_len"]),
		};
		var pathsData = route["paths"] as JArray;
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

	}
	else
	{
            Console.WriteLine("testData.ProgramV4VxlanRoutes is null");
	}
    }
}
