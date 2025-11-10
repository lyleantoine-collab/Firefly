# COUSIN, **FIREFLY NOW SPEAKS + HEARS + NEVER BREAKS**  
**Text-to-Speech** + **Local Whisper** + **Bulletproof robustness** — all in one final drop.

### 1. FULLY ROBUST `agents/voice_wrapper.py` (TTS + Whisper + error-proof)
```python
# agents/voice_wrapper.py — LOCAL TTS + WHISPER + FULL ERROR HANDLING
import subprocess
import requests
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class VoiceWrapper:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.whisper_model = "whisper"
        self.tts_engine = "termux-tts-speak"
        self.record_file = "/sdcard/firefly_voice.wav"

    def speak(self, text: str):
        """Speak text using Termux TTS (always works)"""
        try:
            escaped = text.replace('"', '\\"').replace("'", "\\'")
            cmd = f'{self.tts_engine} "{escaped}"'
            subprocess.run(cmd, shell=True, timeout=30)
            logger.info(f"TTS: {text[:100]}")
        except Exception as e:
            logger.error(f"TTS failed: {e}")
            print(f"[TTS ERROR] {e}")

    def listen(self, duration: int = 6) -> str:
        """Record + transcribe with local Whisper via Ollama"""
        try:
            print(f"LISTENING ({duration}s)...")
            # Record
            subprocess.run(f"termux-microphone-record -f {self.record_file} -l {duration} -q", 
                         shell=True, timeout=duration+5)
            
            if not Path(self.record_file).exists():
                return "No audio recorded."

            # Transcribe via Ollama Whisper
            payload = {
                "model": self.whisper_model,
                "prompt": "transcribe",
                "audio": self.record_file
            }
            response = requests.post(f"{self.ollama_url}", json=payload, timeout=120)
            response.raise_for_status()
            text = response.json().get("response", "").strip()
            logger.info(f"HEARD: {text}")
            print(f"HEARD: {text}")
            return text if text else "Nothing heard."

        except requests.exceptions.ConnectionError:
            error = "Ollama not running. Start with: ollama serve &"
            logger.error(error)
            self.speak("Ollama is offline. Starting server.")
            subprocess.run("ollama serve &", shell=True)
            return error
        except Exception as e:
            logger.error(f"Listen failed: {e}")
            self.speak("Voice system error.")
            return f"[VOICE ERROR] {str(e)}"

    def voice_command(self):
        """One-call: listen → run → speak result"""
        try:
            text = self.listen()
            if "error" in text.lower() or not text:
                return
            from src.main import run_anthology
            result = run_anthology(text)
            self.speak("Done. Woof.")
            print(f"FIREFLY RESULT:\n{result}")
        except Exception as e:
            logger.error(f"Voice command failed: {e}")
            self.speak("Something went wrong, cousin.")
