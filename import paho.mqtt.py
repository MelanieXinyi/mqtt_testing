import paho.mqtt.client as mqtt
import queue
import threading
import time
# Initialize queue for messages
message_queue = queue.Queue()
# MQTT callback when a message is received
def on_message(client, userdata, msg):
    message_queue.put(msg)
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
# MQTT setup
client = mqtt.Client()
client.on_message = on_message
# Connect to MQTT broker
broker_address = "your_broker_address"  # Replace with your broker address
port = 1883  # Default MQTT port
client.connect_async(broker_address, port=port)
# Subscribe to a topic
topic = "your/topic"  # Replace with your desired topic
client.subscribe(topic)
# Function to process messages from the queue
def process_queue():
    while True:
        try:
            msg = message_queue.get(timeout=1)  # Wait for a message with a timeout
            # Process the message here
            print(f"Processing message: {msg.payload.decode()}")
            message_queue.task_done()
        except queue.Empty:
            # No message in the queue, continue
            continue
        except Exception as e:
            print(f"An error occurred while processing the queue: {e}")
# Start the message processing thread
queue_thread = threading.Thread(target=process_queue, daemon=True)
queue_thread.start()
# Start the MQTT client loop (non-blocking)
client.loop_start()
# Keep the main thread running to allow message processing
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.loop_stop()
    print("MQTT loop stopped.")






