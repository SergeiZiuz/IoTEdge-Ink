using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json.Schema;

namespace SmartHive.Common.Data
{
    public class ScheduleData
    {
        public string RoomId { get; set; }
        public Appointment[] Schedule { get; set; }
    }
    public class Appointment
    {
         public string StartTime { get; set; }
         public string EndTime { get; set; }
         public string Location { get; set; }
		 public string Title { get; set; }			
		 public string Category { get; set; }
        public string MeetingExternalLink { get; set; }

    }

    public static class ScheduleUpdateEventSchema
    {
        private static JSchema schemaJson = JSchema.Parse(
                        @"{  
                              'type': 'object',
                              'properties': {
                                'RoomId': {
                                  'type': 'string'
                                },
                                'Schedule': {
                                  'type': 'array',
                                  'items': {}
                                }
                              },
                              'required': [
                                'RoomId',
                                'Schedule'
                              ]
                            }");
        //   new Newtonsoft.Json.Schema.Generation.JSchemaGenerator().Generate(typeof(OnScheduleUpdateEventArgs[]));

        public static bool IsValid(string json)
        {
            try
            {
                JObject jObject = JObject.Parse(json);
                return jObject.IsValid(schemaJson);
            }
            catch
            {
                return false;
            }

        }
    }
}
