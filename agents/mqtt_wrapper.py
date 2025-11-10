```python
# agents/mqtt_wrapper.py — FULL MQTT (for ANY broker)
import paho.mqtt.client as mqtt
import json
import logging
import threading

logger = logging.getLogger(__name__)

class MQTTWrapper:
    def __init__(self, broker="localhost", port=1883, username=None, password=None):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        if username:
            self.client.username_pw_set(username, password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.connected = False
        threading.Thread(target=self.client.loop_forever, daemon=True).start()
        self.client.connect_async(broker, port, 60)

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            logger.info("MQTT CONNECTED")
        else:
            logger.error(f"MQTT CONNECT FAILED: {rc}")

    def _on_message(self, client, userdata, msg):
        logger.info(f"MQTT RECV: {msg.topic} → {msg.payload.decode()}")

    def publish(self, topic: str, payload: str):
        try:
            if not self.connected:
                self.client.reconnect()
            result = self.client.publish(topic, payload)
            logger.info(f"MQTT SENT: {topic} → {payload}")
            return f"MQTT {topic} = {payload}"
        except Exception as e:
            logger.error(f"MQTT publish failed: {e}")
            return f"[MQTT ERROR] {e}"
