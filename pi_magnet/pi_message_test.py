import time

from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=stg-iot-ws-hub.azure-devices.net;DeviceId=VS_code_device;SharedAccessKey=h7UWaHU15JbSuK4xtsvOhnqdwKUaXsL/H8TLbW418oE="

# Define the JSON message to send to IoT Hub.
From = "Pi"
To = "Azure"
MSG_TXT = '{{"From": {first},"To": {second}}}'

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
            first = From
            second = To
            msg_txt_formatted = MSG_TXT.format(first=first, second=second)
            message = Message(msg_txt_formatted)

            # Send the message.
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(3)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()