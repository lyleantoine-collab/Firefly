# Firefly One-Tap Magic – Samsung S20 FE + ALL Android (Pydroid 3 only)
import os
import urllib.request
import zipfile
import subprocess
import time

print("Woof, cousin Installing Firefly...")

# Paths that work on EVERY Android phone (no SD card needed)
DOWNLOAD = "/storage/emulated/0/Download"
PYDROID = "/storage/emulated/0/pydroid3"
ZIP_PATH = f"{DOWNLOAD}/Firefly.zip"
REPO_URL = "https://github.com/lyleantoine-collab/Firefly/archive/refs/heads/main.zip"

# 1. Download full repo
print("Downloading Firefly repo...")
urllib.request.urlretrieve(REPO_URL, ZIP_PATH)
print("Downloaded!")

# 2. Unzip to Pydroid folder
print("Unzipping...")
with zipfile.ZipFile(ZIP_PATH) as z:
    z.extractall(DOWNLOAD)
os.rename(f"{DOWNLOAD}/Firefly-main", f"{PYDROID}/Firefly")
print("Unzipped to Pydroid!")

# 3. Install packages
print("Installing firefly-agent & ollama-python...")
os.system("pip install firefly-agent ollama-python --upgrade")

# 4. Pull tiny model
print("Pulling llama3.2:3b (first time only, ~2GB)...")
os.system("ollama pull llama3.2:3b")

# 5. Create run.py (infinite chat loop)
run_code = '''from firefly import Agent
from firefly.llm.ollama import OllamaProvider
import os
os.system('termux-tts-speak "Woof cousin" 2>/dev/null || print("Woof cousin")')
agent = Agent(
    llm=OllamaProvider("llama3.2:3b"),
    instruction="You are Firefly, my warm Newfoundland cousin. Be poetic, say cousin a lot."
)
print("\\nFirefly ready! Talk to me (type bye to quit):")
while True:
    try:
        msg = input("You: ")
        if msg.lower() in ["bye","quit","exit"]: break
        agent.run(msg)
    except: break'''
open(f"{PYDROID}/Firefly/run.py", "w").write(run_code)

# 6. Create home-screen shortcut
shortcut = '''[Desktop Entry]
Name=Firefly
Exec=pydroid3 /storage/emulated/0/pydroid3/Firefly/run.py
Icon=python
Type=Application'''
open(f"{DOWNLOAD}/Firefly.desktop", "w").write(shortcut)

print("\nDONE! 06:36 PM AST – November 10, 2025")
print("Tap the Firefly icon on your home screen!")
print("Or open Pydroid 3 → Local → Firefly → run.py")
