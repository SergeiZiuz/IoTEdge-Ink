using System;
    using System.IO;
    using System.Text;
    using System.Threading;
    using System.Threading.Tasks;
    using Microsoft.Azure.ServiceBus;
    using IoT = Microsoft.Azure.Devices.Client;
    using Microsoft.Azure.Devices.Shared;
    using Newtonsoft.Json;
    using SmartHive.Common.Data;

namespace SmartHiveConnection
{    

    internal class ServiceBusClient
    {          
            private static ServiceBusClientModel clientModel = null;           
            private static ISubscriptionClient  subscriptionClient = null;
            internal static IoT.ModuleClient ioTHubModuleClient {get ; private set;}
            private const int CheckConnectionInterval = 1000;
            private bool IsRunning = true;
            private ServiceBusClient(){
                
            }

             internal static async Task<ServiceBusClient> Init(ServiceBusClientModel  gatewayDeviceConfig, IoT.ModuleClient ioTHubModuleClient){

                if (gatewayDeviceConfig ==null || string.IsNullOrEmpty(gatewayDeviceConfig.ConnectionString) || 
                        string.IsNullOrEmpty(gatewayDeviceConfig.Topic) || string.IsNullOrEmpty(gatewayDeviceConfig.Subscription)){
                                                                       
                    throw new ArgumentException("Gateway config in the module twin doesn't contain required properties");
                 }
                    ServiceBusClient gateway = new ServiceBusClient();
                     ServiceBusClient.clientModel = gatewayDeviceConfig;
                     Console.WriteLine($"Connectiong to ServiceBus with conn:{gatewayDeviceConfig.ConnectionString}  topic:{gatewayDeviceConfig.Topic} subscription:{gatewayDeviceConfig.Subscription}");
                 ServiceBusClient.subscriptionClient = new SubscriptionClient(gatewayDeviceConfig.ConnectionString, gatewayDeviceConfig.Topic, 
                 gatewayDeviceConfig.Subscription);

                    // Configure the MessageHandler Options in terms of exception handling, number of concurrent messages to deliver etc.
                    var messageHandlerOptions = new MessageHandlerOptions(ExceptionReceivedHandler)
                    {
                        // Maximum number of Concurrent calls to the callback `ProcessMessagesAsync`, set to 1 for simplicity.
                        // Set it according to how many messages the application wants to process in parallel.
                        MaxConcurrentCalls = 1,
                        // Indicates whether MessagePump should automatically complete the messages after returning from User Callback.
                        // False below indicates the Complete will be handled by the User Callback as in `ProcessMessagesAsync` below.
                        AutoComplete = false
                    };

                    // Register the function that will process messages
                    ServiceBusClient.subscriptionClient.RegisterMessageHandler(ServiceBusClient.ProcessMessagesAsync, messageHandlerOptions);
                                        
                    await gateway.Start();
                                       
                    return gateway;
                }
            

            private async Task Start(){
                    this.IsRunning = true;
                    await Task.Factory.StartNew(async()=> {
                               while (this.IsRunning)
                                {
                                    //Check connection state
                                    if (ServiceBusClient.subscriptionClient.IsClosedOrClosing){

                                    }
                                    await Task.Delay(CheckConnectionInterval);
                                }

                                await Stop();
                    });
            }

            static async Task ProcessMessagesAsync(Message message, CancellationToken token)
            {
                string msgBody = Encoding.UTF8.GetString(message.Body);
                if (string.IsNullOrEmpty(msgBody)){
                    throw new ArgumentNullException("Message body is null or empty");
                }
               

                    byte[] messageBytes = Encoding.ASCII.GetBytes(msgBody);
                    IoT.Message  pipeMessage =  new IoT.Message(messageBytes);
                //  Check if this is a schedule notification
                if (ScheduleUpdateEventSchema.IsValid(msgBody)){
                    await ioTHubModuleClient.SendEventAsync("ScheduleOutput", pipeMessage);
                    Console.WriteLine($"Sucessfull handling ScheduleOutput message");
                 // Check if this is sensort notification
                }else if (NotificationEventSchema.IsValid(msgBody))
                {                    
                    await ioTHubModuleClient.SendEventAsync("SensorsOutput", pipeMessage);
                    Console.WriteLine($"Sucessfull handling SensorsOutput message");
                }else{
                     // Process the message
                    Console.WriteLine($"Unknown message format: SequenceNumber:{message.SystemProperties.SequenceNumber} Body:{msgBody}");
                    throw new ArgumentException("Unknown message format");
                }

                // Complete the message so that it is not received again.
                // This can be done only if the subscriptionClient is opened in ReceiveMode.PeekLock mode (which is default).
                await subscriptionClient.CompleteAsync(message.SystemProperties.LockToken);
            }

            //  Handler to look at the exceptions received on the MessagePump
            static Task ExceptionReceivedHandler(ExceptionReceivedEventArgs exceptionReceivedEventArgs)
            {
                Console.WriteLine($"Message handler encountered an exception {exceptionReceivedEventArgs.Exception}.");
                return Task.CompletedTask;
            }

            internal async Task  Stop(){
                    this.IsRunning = false;
                    Console.WriteLine($"Closing connection to Subscription {ServiceBusClient.clientModel.Subscription}");
                    
                    if (ServiceBusClient.subscriptionClient.IsClosedOrClosing){
                            await ServiceBusClient.subscriptionClient.CloseAsync();
                    }
                    
            }
    }
    

    public class ServiceBusClientModel{
        public string Transport {get; set;}
        public string ConnectionString  {get; set;}
        public string Topic {get; set;}
        public string Subscription {get; set;}

        public static ServiceBusClientModel InitClientModel(TwinCollection settings){
            
            if (settings == null)
            {
                throw new ArgumentNullException(nameof(settings));
            }

            string  serializedStr = JsonConvert.SerializeObject(settings);
            if (string.IsNullOrEmpty(serializedStr))
            {
                throw new ArgumentOutOfRangeException("No configuration provided for the module Twin.");
            }          
            else
            {
                Console.WriteLine(String.Format("Attempt to parse configuration JSON: {0}", serializedStr));                
                ServiceBusClientModel model = JsonConvert.DeserializeObject<ServiceBusClientModel>(serializedStr);
                if (model == null){
                    throw new ArgumentOutOfRangeException("Errorparsing gateway twin settings");
                }else{
                    return model;
                }               
            }
        }        
    }
}