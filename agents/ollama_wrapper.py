# agents/ollama_wrapper.py
import requests

class OllamaWrapper:
    def __init__(self, model_name="llama3.2"):
        self.model = model_name
        self.url = "http://localhost:11434/api/generate"

    def call(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.url, json=payload, timeout=120)
            response.raise_for_status()
            return response.json()["response"].strip()
        except Exception as e:
            return f"[OLLAMA ERROR] {str(e)}"
