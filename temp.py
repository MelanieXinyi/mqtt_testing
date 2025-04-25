import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
import time

broker_address = "localhost"  
broker_port = 1883

def on_disconnect(client, userdata, flags, reason_code, properties):
    print(f"Disconnected with result code {reason_code}")
    while True:
            try:
                client.reconnect()
                break
            except Exception as e:
                print(f"Reconnect failed: {e}")
                time.sleep(5)  # Wait before retrying

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("subscribers")
    
def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))
    # client.disconnect()


client = mqtt.Client(client_id = "nabc25/CU_Hyperloop_differentID1", callback_api_version=CallbackAPIVersion.VERSION2)

client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(broker_address, broker_port)

client.loop_forever()



