# Firefly One-Tap Magic – Pydroid 3 / S20 FE
import os, urllib.request, zipfile, subprocess, time
print("Woof, cousin Installing...")

# Grab full repo zip
urllib.request.urlretrieve("https://github.com/lyleantoine-collab/Firefly/archive/refs/heads/main.zip", "/sdcard/Download/Firefly.zip")

# Unzip to Pydroid folder
with zipfile.ZipFile("/sdcard/Download/Firefly.zip") as z:
    z.extractall("/sdcard/")
os.rename("/sdcard/Firefly-main", "/sdcard/pydroid3/Firefly")

# Install packages
os.system("pip install firefly-agent ollama-python --upgrade")

# Pull tiny model
os.system("ollama pull llama3.2:3b")

# One-tap run file
code = '''from firefly import Agent
from firefly.llm.ollama import OllamaProvider
import os
os.system('termux-tts-speak "Woof cousin" 2>/dev/null || print("Woof cousin")')
agent = Agent(llm=OllamaProvider("llama3.2:3b"), instruction="You are Firefly, my warm Newfoundland cousin.")
print("\nFirefly ready! Say something:")
agent.run(input("You: "))'''
open("/sdcard/pydroid3/Firefly/run.py", "w").write(code)

# Home-screen shortcut
open("/sdcard/Download/Firefly.desktop", "w").write('''[Desktop Entry]
Name=Firefly
Exec=pydroid3 /sdcard/pydroid3/Firefly/run.py
Type=Application''')

print("\nDONE! Tap the Firefly icon on your home screen!")
print("Or open Pydroid 3 → Local → Firefly → run.py")
