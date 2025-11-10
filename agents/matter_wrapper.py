# agents/matter_wrapper.py — MATTER VIA HOME ASSISTANT
import requests
import logging

logger = logging.getLogger(__name__)

class MatterWrapper:
    def __init__(self, ha_url="http://homeassistant.local:8123", token="YOUR_TOKEN"):
        self.url = ha_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def control(self, entity_id: str, command: str, value=None):
        try:
            domain = "light" if "light" in entity_id else "switch"
            service = command
            payload = {"entity_id": entity_id}
            if value is not None:
                payload["brightness_pct"] = value if command == "turn_on" else 0

            response = requests.post(
                f"{self.url}/api/services/{domain}/{service}",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            logger.info(f"MATTER: {entity_id} → {command}")
            return f"Matter {entity_id} {command}"
        except Exception as e:
            logger.error(f"Matter failed: {e}")
            return f"[MATTER ERROR] {e}"
