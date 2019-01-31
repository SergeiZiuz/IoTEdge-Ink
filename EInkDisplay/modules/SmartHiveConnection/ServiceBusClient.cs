using System;
    using System.IO;
    using System.Text;
    using System.Linq;
    using System.Threading;
    using System.Threading.Tasks;
    using Microsoft.Azure.ServiceBus;
    using IoT = Microsoft.Azure.Devices.Client;
    using Microsoft.Azure.Devices.Shared;
    using System.Collections.Generic;
    using Newtonsoft.Json;
    using SmartHive.Common.Data;
    using System.Globalization;

namespace SmartHiveConnection
{    

    internal class ServiceBusClient
    {          
            private static ServiceBusClientModel clientModel = null;           
            private static ISubscriptionClient  subscriptionClient = null;
            internal static IoT.ModuleClient ioTHubModuleClient {get ; private set;}

          //  private bool IsRunning = true;
            private ServiceBusClient(){
                
            }

             internal static ServiceBusClient Init(ServiceBusClientModel  gatewayDeviceConfig, IoT.ModuleClient ioTHubModuleClient){

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
                    ServiceBusClient.ioTHubModuleClient = ioTHubModuleClient;           
                    
                   // await gateway.Start();
                                       
                    return gateway;
                }
            

            static async Task ProcessMessagesAsync(Message message, CancellationToken token)
            {
                try{
                    string msgBody = Encoding.UTF8.GetString(message.Body);
                    if (string.IsNullOrEmpty(msgBody)){
                        throw new ArgumentNullException("Message body is null or empty");
                    }
                

                       
                    //  Check if this is a schedule notification
                    string timestamp = DateTime.Now.ToString("dd/MM/yy hh:mm:ss");
                    if (ScheduleUpdateEventSchema.IsValid(msgBody)){
                        
                        ScheduleData eventData = JsonConvert.DeserializeObject<ScheduleData>(msgBody);
                            // Remove expired events
                        eventData.Schedule = ServiceBusClient.FilterAppointments(eventData);                

                        msgBody = JsonConvert.SerializeObject(eventData);

                        byte[] messageBytes = Encoding.UTF8.GetBytes(msgBody);

                        IoT.Message  pipeMessage =  new IoT.Message(messageBytes);

                        await ioTHubModuleClient.SendEventAsync("ScheduleOutput", pipeMessage);
                        Console.WriteLine($"{timestamp} sucessfully handling ScheduleOutput message as {msgBody}");
                    // Check if this is sensort notification
                    }else if (NotificationEventSchema.IsValid(msgBody))
                    {   
                        
                        //TODO: process events from sensors
                        //await ioTHubModuleClient.SendEventAsync("SensorsOutput", pipeMessage);
                        Console.WriteLine($"{timestamp} sucessfully handling SensorsOutput message {msgBody}");
                    }else{
                        // Process the message
                        Console.WriteLine($"Unknown message format: SequenceNumber:{message.SystemProperties.SequenceNumber} Body:{msgBody}");
                        throw new ArgumentException("Unknown message format");
                    }
                }catch(Exception ex){
                        Console.WriteLine($"Error processing message: {ex.Message} {ex.StackTrace}");
                }finally{
                        // Complete the message so that it is not received again.
                        // This can be done only if the subscriptionClient is opened in ReceiveMode.PeekLock mode (which is default).
                        await subscriptionClient.CompleteAsync(message.SystemProperties.LockToken);
                }
            }

            //  Handler to look at the exceptions received on the MessagePump
            static Task ExceptionReceivedHandler(ExceptionReceivedEventArgs exceptionReceivedEventArgs)
            {
                Console.WriteLine($"Message handler encountered an exception {exceptionReceivedEventArgs.Exception}.");
                return Task.CompletedTask;
            }

            internal async Task  Stop(){
                  //  this.IsRunning = false;
                    Console.WriteLine($"Closing connection to Subscription {ServiceBusClient.clientModel.Subscription}");
                    
                    if (ServiceBusClient.subscriptionClient.IsClosedOrClosing){
                            await ServiceBusClient.subscriptionClient.CloseAsync();
                    }
                    
            }

        private static Appointment[] FilterAppointments(ScheduleData eventData)
        {
            if (eventData == null || eventData.Schedule == null)
                return new Appointment[0];

                int inEventsCnt = eventData.Schedule.Count();

                DateTime expirationTime = DateTime.Now.AddSeconds(ServiceBusClient.clientModel.eventsExpiration * -1);
                //return all engagements  and not finished yet or finished not leater then eventsExpiration minutes
                Appointment[] retVal = eventData.Schedule.Where<Appointment>(a => 
                        expirationTime.CompareTo(DateTime.ParseExact(a.EndTime, ServiceBusClient.clientModel.DateTimeFormat, CultureInfo.InvariantCulture)) <= 0).ToArray<Appointment>();

                int outEventsCnt = retVal.Count();

                Console.WriteLine($"Filtered { inEventsCnt  - outEventsCnt} from {inEventsCnt} input events.\n Event removed after {ServiceBusClient.clientModel.eventsExpiration} seconds\n");

                return retVal;        
        }
    }
    

    public class ServiceBusClientModel{
        public string Transport {get; set;}
        public string ConnectionString  {get; set;}
        public string Topic {get; set;}
        public string Subscription {get; set;}
        public string DateTimeFormat {get; set; } = @"dd\/MM\/yyyy HH:mm";
        
        public int  CheckConnectionInterval {get; set;} =1000;

        /** If event finished it will be removed from display after this period of time  */
        public int  eventsExpiration {get; set;} =5*60*60;

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