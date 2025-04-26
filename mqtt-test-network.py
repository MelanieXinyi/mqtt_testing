import paho.mqtt.client as mqtt #pip install paho-mqtt
import json
import time
import datetime
import math

import socket
import subprocess

class Publisher:  
    def __init__(self):
        self.broker_address = "localhost"  
        self.broker_port = 1883
        self.topic = "test" 
        self.broker_client = mqtt.Client(client_id="coolid") #every program's broker client id should be different!
        
    def connect_broker(self):    
        self.broker_client.connect_async(self.broker_address, self.broker_port)
        # Start the MQTT loop in a background thread
        self.broker_client.loop_start()

    def on_disconnect(client, userdata, flags, reason_code, properties):
        print(f"Disconnected with result code {reason_code}")
        while True:
                try:
                    client.reconnect()
                    break
                except Exception as e:
                    print(f"Reconnect failed: {e}")
                    time.sleep(5)  # Wait before retrying

    def ensure_connection(self):
        # Ensure connection is established
        while not self.broker_client.is_connected():
            print("Waiting for MQTT connection...")
            time.sleep(1)  # Sleep for a while and check again
        print("Connected to the broker!")

    def loadJson(self):
        with open('values.json', 'r') as f:
            self.broker_data = json.load(f)

    def publish(self, counter):
        self.broker_data["timestamp"] = math.ceil(datetime.datetime.now().timestamp()) * 1000 #unix time stamp 
        self.broker_data["mining"] = counter
        self.broker_data["chainage"] = counter
        self.broker_data["easting"] = counter
        self.broker_data["northing"] = counter
        self.broker_data["elevation"] = counter
        self.broker_data["roll"] = counter
        self.broker_data["pitch"] = counter
        self.broker_data["heading"] = counter
        self.broker_data["extra"]["Test: Estop"] = bool(1)

        msg = json.dumps(self.broker_data)          
        self.publish_msg(msg)

    def publish_msg(self, msg):
        result = self.broker_client.publish(self.topic, msg)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Sent `{msg}` to topic `{self.topic}`")
        else:
            print(f"Failed to send message {msg} to topic {self.topic}")

    def is_connected(self):
        return self.broker_client.is_connected()
    
    def is_connected_to_network(self):
        #temporarily implementing this with checking for internet connection rather than ethernet
        #rework this once you get a router :)
        try:
        # Try to create a socket connection to Google's public DNS server (8.8.8.8)
        # on port 53 (DNS port).  A timeout of 5 seconds is used.
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
        # An OSError (which includes socket.gaierror, socket.timeout, and others)
        # will be raised if the connection attempt fails.  This could be due to
        # no network connectivity, the server being unreachable, or a firewall.
            return False

        

if __name__ == "__main__":
    counter = 0
    publisher = Publisher()
    publisher.connect_broker()
    publisher.ensure_connection()
    publisher.loadJson()
    while True:
        if(publisher.is_connected_to_network()):
            publisher.publish(counter)
            counter += 1
        else:
            print("NOT CONNECTED, pausing data publishing")
        
        time.sleep(1)

