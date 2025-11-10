# agents/voice_command.py
import subprocess
from agents.ollama_wrapper import OllamaWrapper
from src.main import run_anthology

class VoiceCommand:
    def listen_and_run(self):
        print("LISTENING FOR VOICE COMMAND...")
        # Record 5 seconds of audio
        subprocess.run("termux-microphone-record -f /sdcard/voice.wav -l 5", shell=True)
        # Convert to text via Ollama (whisper.cpp via Ollama)
        ollama = OllamaWrapper("whisper")
        text = ollama.call("transcribe /sdcard/voice.wav")
        print(f"HEARD: {text}")
        run_anthology(text)
