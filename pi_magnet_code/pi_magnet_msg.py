import time
import RPi.GPIO as io
import sys
import json

from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=stg-iot-ws-hub.azure-devices.net;DeviceId=raspberry_pi_stg;SharedAccessKey=zI7H5DOYX8ocxVUuLX40UUkrCLCSxuHccoUnQ2PRv10="

# Set Broadcom mode so we can address GPIO pins by number.
io.setmode(io.BCM)

wheelpin = 18
io.setup(wheelpin, io.IN, pull_up_down=io.PUD_UP) 

# Define the JSON message to send to IoT Hub.
messageEpoch = time.time()
deviceID = "Raspberry_PI_STG"
magnet = 0
MSG_TXT = '{{"messageEpoch": {msg_epoch},"deviceID": {dev_id},"magnet": {magnet},"pinNum": {pin_num}}}'

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        while True:
            # Build the message with simulated telemetry values.
            messageEpoch = time.time()
            magnet = 0
            if (io.input(wheelpin) == 0):
                magnet = 1
            msg_txt_formatted = MSG_TXT.format(msg_epoch=messageEpoch, dev_id=deviceID, magnet=magnet, pin_num=wheelpin)
            message = Message(json.dumps(msg_txt_formatted))
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
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()