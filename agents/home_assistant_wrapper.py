# agents/home_assistant_wrapper.py
import requests
import logging

logger = logging.getLogger(__name__)

class HomeAssistantWrapper:
    def __init__(self, url="http://homeassistant.local:8123", token="YOUR_LONG_LIVED_TOKEN"):
        self.url = url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def call_service(self, domain: str, service: str, entity_id: str = None, data: dict = None):
        try:
            url = f"{self.url}/api/services/{domain}/{service}"
            payload = {"entity_id": entity_id} if entity_id else {}
            if data:
                payload.update(data)
            response = requests.post(url, headers=self.headers, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"HA: {domain}.{service} → {entity_id}")
            return f"Home Assistant: {service.replace('_', ' ')} {entity_id or ''}"
        except Exception as e:
            logger.error(f"HA failed: {e}")
            return f"[HA ERROR] {e}"
