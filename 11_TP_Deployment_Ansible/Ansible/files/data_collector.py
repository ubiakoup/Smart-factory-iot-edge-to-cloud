import yaml
import time
import json
import logging
from opcua import Client
from opcua import ua
import paho.mqtt.client as mqtt

# ====================================
# Logging configuration
# ====================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ====================================
# Load configuration
# ====================================

with open("config.yml") as f:
    config = yaml.safe_load(f)

opc_url = config["opcua"]["url"]
mqtt_broker = config["mqtt"]["broker"]
mqtt_port = config["mqtt"]["port"]

# ====================================
# MQTT connection
# ====================================

def connect_mqtt():

    client = mqtt.Client()

    while True:
        try:
            client.connect(mqtt_broker, mqtt_port)
            logging.info("Connected to MQTT broker")
            return client
        except Exception as e:
            logging.error(f"MQTT connection failed: {e}")
            time.sleep(5)


mqtt_client = connect_mqtt()
mqtt_client.loop_start()

# ====================================
# OPC UA connection
# ====================================

def connect_opcua():

    while True:
        try:
            client = Client(opc_url)
            client.connect()
            logging.info("Connected to OPC UA Server")
            return client
        except Exception as e:
            logging.error(f"OPCUA connection failed: {e}")
            time.sleep(5)


opc_client = connect_opcua()

# ====================================
# Load nodes from config
# ====================================

nodes = {}

for plc, tags in config["factory"].items():

    nodes[plc] = {}

    for tag, nodeid in tags.items():

        try:
            node = opc_client.get_node(nodeid)
            nodes[plc][tag] = node
        except Exception as e:
            logging.error(f"Failed to load node {nodeid}: {e}")

logging.info("Nodes loaded from config")

# ====================================
# Subscription handler
# ====================================

class SubHandler:

    def datachange_notification(self, node, val, data):

        try:

            nodeid = node.nodeid.to_string()

            for plc, tags in nodes.items():

                for tag, n in tags.items():

                    if n.nodeid.to_string() == nodeid:

                        topic = f"factory/{plc}/{tag}"

                        payload = {
                            "plc": plc,
                            "tag": tag,
                            "value": val,
                            "timestamp": time.time()
                        }

                        mqtt_client.publish(topic, json.dumps(payload))                       

                        logging.info(f"Published -> {topic}: {val}")

        except Exception as e:
            logging.error(f"Publish error: {e}")


handler = SubHandler()

# ====================================
# Create subscription
# ====================================

subscription = opc_client.create_subscription(500, handler)

for plc in nodes:

    for tag, node in nodes[plc].items():

        try:

            subscription.subscribe_data_change(node)

            logging.info(f"Subscribed: {plc}/{tag}")

        except Exception as e:

            logging.error(f"Subscription failed {plc}/{tag}: {e}")

# ====================================
# Keep collector alive
# ====================================

while True:

    try:
        time.sleep(1)

    except KeyboardInterrupt:
        break

    except Exception as e:

        logging.error(f"Runtime error: {e}")

        try:
            opc_client.disconnect()
        except:
            pass

        opc_client = connect_opcua()