import paho.mqtt.client as mqtt #pip install paho-mqtt
import json
import time
import datetime
import math


class Publisher:  
    def __init__(self):
        self.broker_address = "localhost"  
        self.broker_port = 1883
        self.topic = "test" 
        self.broker_client = mqtt.Client(client_id="nabc25/CU_Hyperloop")
        self.connected_to_broker = False
        self.data_queue = []
        
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
        self.connected_to_broker = True

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

if __name__ == "__main__":
    counter = 0
    publisher = Publisher()
    publisher.connect_broker()
    publisher.ensure_connection()
    publisher.loadJson()
    while True:
        if(publisher.is_connected()):
            publisher.publish(counter)
            counter += 1
        else:
            print("NOT CONNECTED, pausing data publishing")
        
        time.sleep(3)

