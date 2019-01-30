#!/usr/bin/python
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import drawingDisplay
import random
import time
import sys
import iothub_client
import json
# pylint: disable=E0611
from iothub_client import IoTHubModuleClient, IoTHubClientError, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubModuleClient.send_event_async.
# By default, messages do not expire.
MESSAGE_TIMEOUT = 10000

# Choose HTTP, MQTT or  as transport protocol.  Currently only MQTT is supported.
PROTOCOL = IoTHubTransportProvider.MQTT

DISPLAY_DRIVER = drawingDisplay.DrawingDisplay("Room Title","%d/%m/%Y %H:%M")

# receive_schedule_message_callback is invoked when message with room schedule data arrives
def receive_schedule_message_callback(message, hubManager):
    
    try:
        message_buffer = message.get_bytearray()
        size = len(message_buffer)
        message_text = message_buffer[:size].decode('utf-8')

        room_schedule = json.loads(message_text)        

        engagements_cnt = len(room_schedule["Schedule"])
        print ( "%d engagements in the room <<<%s>>>\n" % (engagements_cnt, room_schedule["RoomId"]) )
        
        DISPLAY_DRIVER.drawDisplay(engagements_cnt)

        return IoTHubMessageDispositionResult.ACCEPTED

    except Exception as err:
        print("Error parsing json string %s\n" % err)
        print ( "<<<%s>>> & Size=%d\n" % (message_text, size) )
        

# module_twin_callback is invoked when the module twin's desired properties are updated.
def module_twin_callback(update_state, payload, user_context):
    
    print ( "\nTwin callback called with:\nupdateStatus = %s\npayload = %s\ncontext = %s\n" % (update_state, payload, user_context) )
    data = json.loads(payload)

    

class HubManager(object):

    def __init__(
        self,
        protocol=IoTHubTransportProvider.MQTT):
        self.client_protocol = protocol
        self.client = IoTHubModuleClient()
        self.client.create_from_environment(protocol)

        # set the time until a message times out
        self.client.set_option("messageTimeout", MESSAGE_TIMEOUT)
        
        # Sets the callback when a module twin's desired properties are updated.
        self.client.set_module_twin_callback(module_twin_callback, self)

        # sets the callback when a message arrives on "ScheduleOutput" queue.  
        self.client.set_message_callback("ScheduleInput", receive_schedule_message_callback, self)
        
        # sets the callback when a message arrives on "SensorsOutputInput" queue.  
        #self.client.set_message_callback("SensorsInput", receive_sensor_notification_callback, self)
        print("Initialization done.\n")

    # Forwards the message received onto the next stage in the process.
        # def forward_event_to_output(self, outputQueueName, event, send_context):
        #     self.client.send_event_async(
        #         outputQueueName, event, send_confirmation_callback, send_context)

def main(protocol):
    try:
        print ( "\nPython %s\n" % sys.version )
        print ( "IoT Hub Client for Python" )

        hub_manager = HubManager(protocol)

        print ( "Starting the IoT Hub connection using protocol %s...\n" % hub_manager.client_protocol )
        print ( "Listening incomming room messages.  Press Ctrl-C to exit. \n")

        while True:
            time.sleep(1)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubModuleClient sample stopped" )

if __name__ == '__main__':
    main(PROTOCOL)