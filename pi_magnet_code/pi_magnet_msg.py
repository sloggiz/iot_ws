import time
import RPi.GPIO as io
import sys
import json

from azure.iot.device import IoTHubDeviceClient, Message

# Replace with the corresponding connection string from your device in Az IoT Hub
CONNECTION_STRING = "Paste_your_conn_str_here"

# Set Broadcom mode so we can address GPIO pins by number.
io.setmode(io.BCM)

wheelpin = 18
io.setup(wheelpin, io.IN, pull_up_down=io.PUD_UP) 

# Define the JSON message variables to send to IoT Hub.
messageEpoch = time.time()
deviceID = "Type_your_deviceID_here"
magnet = 0

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        while True:
            # Build the message with magnet telemetry values.
            messageEpoch = time.time()
            magnet = 0
            if (io.input(wheelpin) == 0):
                magnet = 1
            # needs to be a python dict, otherwsie de-serialization errors will occur on Azure side
            msg_dict = {"messageEpoch":messageEpoch, "deviceID":deviceID, "magnet":magnet, "pin_num":wheelpin}
            message = Message(json.dumps(msg_dict))
            # ensure proper encoding and content type are enforced (again to avoid de-serialization issues)
            message.content_encoding = "utf-8"
            message.content_type = "application/json"

            # Send the message.
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(1)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "Azure IoT Workshop - Raspberry PI device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()