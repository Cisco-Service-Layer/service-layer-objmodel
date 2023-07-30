using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using Grpc.Core;
using Grpc.Net.Client;
using Newtonsoft.Json;
using System.IO;
using ServiceLayer;

public class TestVxlan
{
    public Dictionary<string, object> register_vrfs { get; set; }
    public Dictionary<string, object> get_registered_vrfs { get; set; }
    public Dictionary<string, object> program_v4_routes { get; set; }
    public Dictionary<string, object> get_v4_routes { get; set; }
    public Dictionary<string, object> program_v6_routes { get; set; }
    public Dictionary<string, object> get_v6_routes { get; set; }
    public Dictionary<string, object> unregister { get; set; }
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
                testData = JsonConvert.DeserializeObject<TestVxlan>(jsonString);
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
        if (!string.IsNullOrEmpty(serverAddress)) {
	    AppContext.SetSwitch("System.Net.Http.SocketsHttpHandler.Http2UnencryptedSupport", true);
            channel = GrpcChannel.ForAddress($"https://{serverAddress}");
            try {
                client = new SLRoutev4Oper.SLRoutev4OperClient(channel);
            }
            catch (Exception ex) {
                Console.WriteLine("Error initializing the client: " + ex.Message);
	        Environment.Exit(1);
            }
        } else {
            Console.WriteLine("Server address is not provided.");
	    Environment.Exit(1);
        }

        // Register the VRFs
        // Create and populate the SLVrfRegMsg for registration.
        var regMsg = new SLVrfRegMsg
        {   
            Oper = SLRegOp.Register,
            VrfRegMsgs =
            {   
                new SLVrfReg
                {   
                    VrfName = "vxlan_red",
                    AdminDistance = 100,
                    VrfPurgeIntervalSeconds = 60
                }
            }
        };

        // Call the SLRoutev4VrfRegOp RPC
        var regResponse = await client.SLRoutev4VrfRegOpAsync(regMsg);

        // Handle the response (not shown here).

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
