```python
# agents/voice_wrapper.py — FINAL VOICE SYSTEM (local + bulletproof)
import subprocess
import requests
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class VoiceWrapper:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.record_file = "/sdcard/firefly_voice.wav"

    def speak(self, text: str):
        """Termux TTS + Ollama TTS fallback"""
        try:
            escaped = text.replace('"', '\\"').replace("'", "\\'")
            cmd = f'termux-tts-speak "{escaped}"'
            subprocess.run(cmd, shell=True, timeout=30)
            logger.info(f"TTS: {text[:100]}")
        except Exception as e:
            logger.warning(f"Termux TTS failed: {e} — trying Ollama TTS")
            try:
                payload = {"model": "llava", "prompt": f"Say this out loud: {text}"}
                requests.post(self.ollama_url, json=payload, timeout=60)
            except:
                print(f"[TTS FAILED] {text}")

    def listen(self, duration: int = 6) -> str:
        """Local Whisper via Ollama (auto-start server)"""
        try:
            print(f"LISTENING ({duration}s)...")
            subprocess.run(f"termux-microphone-record -f {self.record_file} -l {duration} -q", 
                         shell=True, timeout=duration+5)
            
            if not Path(self.record_file).exists():
                return "No audio."

            payload = {
                "model": "whisper",
                "audio": self.record_file
            }
            response = requests.post(self.ollama_url, json=payload, timeout=120)
            response.raise_for_status()
            text = response.json().get("response", "").strip()
            logger.info(f"HEARD: {text}")
            return text or "Nothing heard."

        except requests.exceptions.ConnectionError:
            logger.warning("Ollama offline — starting...")
            subprocess.Popen("ollama serve", shell=True)
            self.speak("Ollama starting up")
            return "Ollama waking up — try again in 10s"
        except Exception as e:
            logger.error(f"Listen failed: {e}")
            self.speak("Voice error")
            return f"[VOICE ERROR] {e}"

    def voice_command(self):
        text = self.listen()
        if "error" not in text.lower():
            from src.main import run_anthology
            result = run_anthology(text)
            self.speak("Done. Woof.")
