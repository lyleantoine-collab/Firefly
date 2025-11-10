# agents/thread_wrapper.py — THREAD PROTOCOL CONTROL (Matter over Thread)
import requests
import logging

logger = logging.getLogger(__name__)

class ThreadWrapper:
    def __init__(self, ha_url="http://homeassistant.local:8123", token="YOUR_TOKEN"):
        self.url = ha_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def control(self, entity_id: str, action: str, value=None):
        # Thread devices appear as Matter in HA
        try:
            domain = "light" if "light" in entity_id else "switch"
            service = f"turn_{action}"
            payload = {"entity_id": entity_id}
            if value is not None:
                payload["brightness_pct"] = value

            response = requests.post(
                f"{self.url}/api/services/{domain}/{service}",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            result = f"Thread {entity_id} {action}"
            logger.info(result)
            return result
        except Exception as e:
            logger.error(f"Thread failed: {e}")
            return f"[THREAD ERROR] {e}"
