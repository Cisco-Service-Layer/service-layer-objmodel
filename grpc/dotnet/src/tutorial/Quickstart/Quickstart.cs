using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Grpc.Core;
using Grpc.Net.Client;
using ObjectStore;
using ServiceLayer;

class GrpcClient 
{
    static async Task Main(string[] args)
    {
        var serverIp = Environment.GetEnvironmentVariable("SERVER_IP");
        var serverPort = Environment.GetEnvironmentVariable("SERVER_PORT");
        
        if (string.IsNullOrEmpty(serverIp) || string.IsNullOrEmpty(serverPort))
        {
            Console.WriteLine("Environment variables SERVER_IP and SERVER_PORT must be set.");
            return;
        }
        
        var serverAddress = $"https://{serverIp}:{serverPort}";

        using var channel = GrpcChannel.ForAddress(serverAddress);
        var client = new ObjectStoreService.ObjectStoreServiceClient(channel);

        // 1. Initialization
        var initResponse = await client.InitializeAsync(new InitializationRequest { Version = "1.0" });
        Console.WriteLine("Initialization Response: " + initResponse.Message);

        // 2. Run a background thread to receive async notifications from the server
        _ = Task.Run(async () =>
        {
            var notifications = client.AsyncNotifications(new Empty());

            await foreach (var notification in notifications.ResponseStream.ReadAllAsync())
            {
                Console.WriteLine("Received notification: " + notification.Message);
            }
        });

        // 3. Perform operations
        var objects = new List<Object>
        {
            new Object { Key = "key1", Data = "data1" },
            new Object { Key = "key2", Data = "data2" }
        };

        // Add operation
        var addResponse = await client.OperateAsync(new OperationRequest
        {
            Operation = OperationType.ADD,
            Objects = { objects }
        });
        Console.WriteLine("Add Response: " + addResponse.Message);

        // Get operation
        var getResponse = await client.OperateAsync(new OperationRequest
        {
            Operation = OperationType.GET,
            Objects = { new Object { Key = "key1" } }
        });
        foreach (var obj in getResponse.Objects)
        {
            Console.WriteLine($"Key: {obj.Key}, Data: {obj.Data}");
        }

        // Other operations...

        // Wait before exit
        Console.WriteLine("Press any key to exit...");
        Console.ReadKey();
    }
}

