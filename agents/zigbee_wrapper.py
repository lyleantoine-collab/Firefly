# agents/zigbee_wrapper.py — BULLETPROOF VERSION
import requests
import logging

logger = logging.getLogger(__name__)

class ZigbeeWrapper:
    def __init__(self, mqtt_url="http://localhost:8080/api/v1"):
        self.url = mqtt_url.rstrip("/")
        self.headers = {"Content-Type": "application/json"}

    def set_device(self, device_id: str, state: str, data: dict = None):
        try:
            payload = data or {"state": state.upper()}
            full_url = f"{self.url}/device/{device_id}"
            response = requests.put(full_url, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            logger.info(f"ZIGBEE: {device_id} → {state}")
            return f"Zigbee {device_id} {state}"
        except requests.exceptions.ConnectionError:
            error = "Zigbee2MQTT offline. Starting..."
            logger.warning(error)
            import subprocess
            subprocess.Popen("zigbee2mqtt", shell=True)
            return "Zigbee2MQTT waking up — try again in 10s"
        except requests.exceptions.HTTPError as e:
            error = f"HTTP {e.response.status_code}: {e.response.text}"
            logger.error(error)
            return f"[ZIGBEE HTTP ERROR] {error}"
        except Exception as e:
            logger.error(f"Zigbee unknown error: {e}")
            return f"[ZIGBEE ERROR] {e}"
