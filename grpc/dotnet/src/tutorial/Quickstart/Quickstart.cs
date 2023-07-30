using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Linq;
using Grpc.Core;
using Grpc.Net.Client;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using Newtonsoft.Json.Linq;
using System.IO;
using ServiceLayer;


public class TestVxlan
{
    public Dictionary<string, object> RegisterV4Vrfs { get; set; }
    public Dictionary<string, object> GetV4Vrfs { get; set; }
//    public Dictionary<string, object> RegisterV6Vrfs { get; set; }
//    public Dictionary<string, object> GetV6Vrfs { get; set; }
//    public Dictionary<string, object> ProgramV4Routes { get; set; }
//    public Dictionary<string, object> GetV4Routes { get; set; }
//    public Dictionary<string, object> ProgramV6Routes { get; set; }
//    public Dictionary<string, object> GetV6Routes { get; set; }
//    public Dictionary<string, object> Unregister { get; set; }
}

class SLClient
{
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
                Console.WriteLine($"Read JSON: {jsonString}");
            
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
                }
                else 
                {
                    Console.WriteLine($"Deserialized to object: {JsonConvert.SerializeObject(testData)}");
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
	if(testData == null) 
	{
                Console.WriteLine("testData is null");
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
	}
	else
	{
            Console.WriteLine("testData.RegisterV4Vrfs is null");
	}


        // Create and populate the SLVrfRegMsg for EOF operation.
        var eofMsg = new SLVrfRegMsg
        {   
            Oper = SLRegOp.Eof
        };

        // Call the SLRoutev4VrfRegOp RPC
        var eofResponse = await client.SLRoutev4VrfRegOpAsync(eofMsg);

        // Handle the response (not shown here).

        // Create and populate the SLVrfRegGetMsg.
        var getMsg = new SLVrfRegGetMsg
        {   
            VrfName = "vxlan_red",
            EntriesCount = 10,
            GetNext = false
        };

        // Call the SLRoutev4VrfRegGet RPC
        var getResponse = await client.SLRoutev4VrfRegGetAsync(getMsg);

        // Handle the response (not shown here).
    }
}
