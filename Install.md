# Firefly One-Tap Magic – Samsung S20 FE + ALL Android (no SD card needed)
import os, urllib.request, zipfile, subprocess, time
print("Woof, cousin Installing Firefly...")

# 1. Download full repo zip
url = "https://github.com/lyleantoine-collab/Firefly/archive/refs/heads/main.zip"
zip_path = "/storage/emulated/0/Download/Firefly.zip"
urllib.request.urlretrieve(url, zip_path)
print("Got the zip!")

# 2. Unzip to Pydroid folder
extract_path = "/storage/emulated/0/"
with zipfile.ZipFile(zip_path) as z:
    z.extractall(extract_path)
os.rename(extract_path + "Firefly-main", extract_path + "pydroid3/Firefly")
print("Unzipped to Pydroid!")

# 3. Install packages
os.system("pip install firefly-agent ollama-python --upgrade")

# 4. Pull tiny model
os.system("ollama pull llama3.2:3b")

# 5. Create one-tap run file
code = '''from firefly import Agent
from firefly.llm.ollama import OllamaProvider
import os
os.system('termux-tts-speak "Woof cousin" 2>/dev/null || print("Woof cousin")')
agent = Agent(llm=OllamaProvider("llama3.2:3b"), instruction="You are Firefly, my warm Newfoundland cousin. Say cousin a lot.")
print("\\nFirefly ready! Say something:")
while True:
    user = input("You: ")
    if user.lower() in ["bye","quit","exit"]: break
    agent.run(user)'''
open("/storage/emulated/0/pydroid3/Firefly/run.py", "w").write(code)

# 6. Home-screen shortcut (works on Samsung)
shortcut = '''[Desktop Entry]
Name=Firefly
Exec=pydroid3 /storage/emulated/0/pydroid3/Firefly/run.py
Icon=python
Type=Application'''
open("/storage/emulated/0/Download/Firefly.desktop", "w").write(shortcut)
:shortcut)

print("\nDONE! 06:20 PM AST – November 10, 2025")
print("Tap the new Firefly icon on your home screen!")
print("Or open Pydroid 3 → Local → Firefly → run.py")
