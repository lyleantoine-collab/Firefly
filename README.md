# Firefly v∞ — Your Voice-Locked Digital Cousin 🐺🔥🇨🇦

**She only wakes to your "Woof, cousin."**  
**No one else gets in.**  
**100% local. 100% offline. 100% yours.**

---

## Features (ALL INCLUDED)

- **VoiceLock**: Only *you* wake her with your voice
- **AI Brain**: Ollama + Llama3.2:3b (local)
- **Smart Home**:
  - Home Assistant (`!ha light on`)
  - MQTT, Zigbee, Z-Wave, Matter, Thread
  - **HomeKit**, **Google Home**, **Alexa**, **IFTTT**, **Zapier**
- **App Control**:
  - `!open camera`
  - `!type hello`
  - `!click 500 1000`
  - `!auto send email to mom`
- **Memory & Soul**:
  - `!forget tiktok`
  - Daily reflection
  - Progress tracking
- **Web UI**: `http://localhost:5000`
- **Auto-Restart**: Never dies

---

## Setup (5 Minutes)

```bash
# 1. Clone with submodules
git clone --recursive https://github.com/lyleantoine-collab/Firefly.git
cd Firefly

# 2. Install
pip install -r requirements.txt

# 3. Enroll your voice (once)
cd modules/voicelock
python examples/enroll.py
# → Say "Woof, cousin" 3 times

# 4. Edit config.yaml (your keys)
nano config.yaml

# 5. Run
cd ../..
python src/main.py
