namespace SmartHiveConnection
{
    using System;
    using System.IO;
    using System.Runtime.InteropServices;
    using System.Runtime.Loader;
    using System.Security.Cryptography.X509Certificates;
    using System.Text;
    using System.Threading;
    using System.Threading.Tasks;
    using Microsoft.Azure.Devices.Client;
    using Microsoft.Azure.Devices.Shared;
    using Microsoft.Azure.Devices.Client.Transport.Mqtt;
   

    class Program
    {        
        public const string ScheduleOutputName = "ScheduleOutput";
        public const string SensorsOutputName = "SensorsOutput";

        private static ServiceBusClient serviceBusClient = null;

        static void Main(string[] args)
        {
            #if IOT_EDGE
            // Install CA certificate
                InstallCert();
            #endif

             InitEdgeModule().Wait();

            // Wait until the app unloads or is cancelled
            var cts = new CancellationTokenSource();
            AssemblyLoadContext.Default.Unloading += (ctx) => cts.Cancel();
            Console.CancelKeyPress += (sender, cpe) => cts.Cancel();
            WhenCancelled(cts.Token).Wait();
        }

        /// <summary>
        /// Handles cleanup operations when app is cancelled or unloads
        /// </summary>
        public static Task WhenCancelled(CancellationToken cancellationToken)
        {
            var tcs = new TaskCompletionSource<bool>();
            cancellationToken.Register(s => ((TaskCompletionSource<bool>)s).SetResult(true), tcs);
            return tcs.Task;
        }

        /// <summary>
        /// Add certificate in local cert store for use by client for secure connection to IoT Edge runtime
        /// </summary>
        static void InstallCert()
        {
            // Suppress cert validation on Windows for now
            if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                return;
            }

            string certPath = Environment.GetEnvironmentVariable("EdgeModuleCACertificateFile");
            if (string.IsNullOrWhiteSpace(certPath))
            {
                // We cannot proceed further without a proper cert file
                Console.WriteLine("Missing path to certificate collection file.");
                throw new InvalidOperationException("Missing path to certificate file.");
            }
            else if (!File.Exists(certPath))
            {
                // We cannot proceed further without a proper cert file
                Console.WriteLine("Missing certificate collection file.");
                throw new InvalidOperationException("Missing certificate file.");
            }
            X509Store store = new X509Store(StoreName.Root, StoreLocation.CurrentUser);
            store.Open(OpenFlags.ReadWrite);
            store.Add(new X509Certificate2(X509Certificate2.CreateFromCertFile(certPath)));
            Console.WriteLine("Added Cert: " + certPath);
            store.Close();
        }

        /// <summary>
        /// Initializes the ModuleClient and sets up the callback to receive
        /// messages containing temperature information
        /// </summary>
        static async Task  InitEdgeModule()
        {
            MqttTransportSettings mqttSetting = new MqttTransportSettings(TransportType.Mqtt_Tcp_Only);
            ITransportSettings[] settings = { mqttSetting };
           /*  AmqpTransportSettings amqpSetting = new AmqpTransportSettings(TransportType.Amqp_Tcp_Only);
            ITransportSettings[] settings = { amqpSetting };*/

            // Open a connection to the Edge runtime
            ModuleClient ioTHubModuleClient = await ModuleClient.CreateFromEnvironmentAsync(settings);
            await ioTHubModuleClient.OpenAsync();
            Console.WriteLine("IoT Hub module client initialized.");

            // Read Module Twin Desired Properties
            Console.WriteLine("Reading module Twin from IoT Hub.");
            var moduleTwin = await ioTHubModuleClient.GetTwinAsync();

            // Parse Twin Json and initialize gateway       
            Console.WriteLine("Starting Gateway controller handler process.");
            ServiceBusClientModel gatewayConfigModel = ServiceBusClientModel.InitClientModel(moduleTwin.Properties.Desired);
            
            serviceBusClient = ServiceBusClient.Init(gatewayConfigModel, ioTHubModuleClient);
            

             // Attach callback for Twin desired properties updates
            await ioTHubModuleClient.SetDesiredPropertyUpdateCallbackAsync(OnDesiredPropertiesUpdate,null);
                       
        }

      

        /// <summary>
        /// Callback to handle Twin desired properties updates�
        /// </summary>
        static async Task OnDesiredPropertiesUpdate(TwinCollection desiredProperties, object userContext)
        {
           
                if (Program.serviceBusClient == null)
                {
                    throw new InvalidOperationException("ServiceBusClient context doesn't exist");
                }
                                
                ModuleClient ioTHubModuleClient = ServiceBusClient.ioTHubModuleClient;
                await serviceBusClient.Stop();
                ServiceBusClientModel gatewayConfigModel = ServiceBusClientModel.InitClientModel(desiredProperties);
                serviceBusClient = ServiceBusClient.Init(gatewayConfigModel, ioTHubModuleClient);

        }
    }
}
