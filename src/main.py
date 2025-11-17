# FIREFLY v∞ FINAL (ZAPIER + ALL + TINY COMMENTS)
import yaml, importlib, logging, time, threading, sys, os
from pathlib import Path
from logging.handlers import RotatingFileHandler

L = importlib.import_module  # Lazy
sys.path.append('modules/voicelock')

# VoiceLock
try:
    lock = L('voicelock').VoiceLock(passphrase="newfoundland-fog-2025")
    print("\nSay 'Woof, cousin'...")
    if not lock.verify(prompt="Woof, cousin"): print("Not you."); exit()
    print("It's you!\n")
except: print("No VoiceLock\n")

# Log
Path(__file__).parent.parent.joinpath("logs").mkdir(exist_ok=True)
logging.basicConfig(handlers=[RotatingFileHandler("logs/firefly.log", maxBytes=1<<20, backupCount=3)], level=logging.INFO)
log = logging.getLogger(__name__); log.info("FIREFLY FINAL")

# Config
cfg = yaml.safe_load(open(Path(__file__).parent.parent / "config.yaml"))

# Cache
C = {}
W = lambda n, **p: C.setdefault(n, getattr(L(f"agents.{n}_wrapper"), f"{n.capitalize()}Wrapper")(**p))

# Run
def run(m):
    log.info(f"In: {m[:40]}")
    c = m

    # Reflection
    try: r = W('reflection'); c = f"[Habit: {r.get_today().get('habit','kind')}]\n{c}"; print(f"\n{r.get_progress_text()}")
    except: pass

    print("\nRUN"); print("="*30)

    # Models
    for md in cfg['models']:
        n = md['name']
        if n in ["device","memory","voice","home_assistant","zigbee","z_wave","mqtt","matter","thread","homekit","googlehome","alexa","ifttt","zapier"]: continue
        print(f"[{n.upper()}]")
        try: c = W(n, **md.get('params',{})).call(c)
        except Exception as e: c += f"\n[ERR {n}] {e}"

    cmd = c.lower()

    # Voice
    try: v = W('voice').VoiceWrapper()
    except: v = None

    # Apps
    try:
        a = W('app_automation').AppAutomation()
        d = W('device').DeviceWrapper()
        if "!auto" in cmd: print(f"AUTO: {a.automate_task(cmd.split('!auto',1)[1].strip())}")
        if "!open" in cmd: d.open_app(cmd.split('!open',1)[1].strip().split()[0])
        if "!type" in cmd: d.type_text(cmd.split('!type',1)[1].strip())
        if "!click" in cmd: xy = cmd.split('!click',1)[1].strip().split()[:2]; d.click(int(xy[0]), int(xy[1]))
    except: pass

    # Memory
    try: if "!forget" in cmd: print(W('memory').MemoryWrapper().forget(cmd.split('!forget',1)[1].strip().split()[0]))
    except: pass

    # Smart Home
    try: if "!ha" in cmd: print(f"HA: {W('home_assistant', url=cfg['home_assistant']['url'], token=cfg['home_assistant']['token']).HomeAssistantWrapper().toggle_entity(cmd.split('!ha',1)[1].strip())}")
    except: pass
    try: if "!mqtt" in cmd: print(f"MQTT: {W('mqtt', host=cfg['mqtt']['host'], port=cfg['mqtt']['port']).MQTTWrapper().publish(cmd.split('!mqtt',1)[1].strip(), 'firefly')}")
    except: pass
    try: if "!zigbee" in cmd: print(f"ZIGBEE: {W('zigbee', port=cfg['zigbee']['port']).ZigbeeWrapper().toggle(cmd.split('!zigbee',1)[1].strip())}")
    except: pass
    try: if "!zwave" in cmd: print(f"Z-WAVE: {W('z_wave', port=cfg['z_wave']['port']).ZWaveWrapper().switch(cmd.split('!zwave',1)[1].strip())}")
    except: pass
    try: if "!matter" in cmd: print(f"MATTER: {W('matter').MatterWrapper().control(cmd.split('!matter',1)[1].strip())}")
    except: pass
    try: if "!thread" in cmd: print(f"THREAD: {W('thread').ThreadWrapper().execute(cmd.split('!thread',1)[1].strip())}")
    except: pass
    try: if "!homekit" in cmd: print(f"HOMEKIT: {W('homekit').HomeKitWrapper().toggle(cmd.split('!homekit',1)[1].strip())}")
    except: pass
    try: if "!google" in cmd: print(f"GOOGLE: {W('googlehome', project_id=cfg['googlehome']['project_id'], credentials=cfg['googlehome']['credentials']).GoogleHomeWrapper().control(cmd.split('!google',1)[1].strip())}")
    except: pass
    try: if "!alexa" in cmd: print(f"ALEXA: {W('alexa', client_id=cfg['alexa']['client_id'], client_secret=cfg['alexa']['client_secret']).AlexaWrapper().control(cmd.split('!alexa',1)[1].strip())}")
    except: pass
    try: if "!ifttt" in cmd: print(f"IFTTT: {W('ifttt', key=cfg['ifttt']['key']).IFTTTWrapper().trigger(cmd.split('!ifttt',1)[1].strip())}")
    except: pass

    # === ZAPIER (NEW)
    try:
        if "!zap" in cmd:
            zap = cmd.split("!zap",1)[1].strip()
            res = W('zapier', api_key=cfg['zapier']['api_key']).ZapierWrapper().run(zap)
            print(f"ZAPIER: {res}")
            if v: v.speak(f"Zap {zap} ran.")
    except Exception as e: log.error(f"Zapier: {e}")

    print("="*30); print("DONE")
    return c

# Web UI
try: threading.Thread(target=W('web_ui').start_web_ui, daemon=True).start(); print("WEB → http://localhost:5000")
except: pass

# Main
if __name__ == "__main__":
    os.system('termux-tts-speak "Woof cousin" 2>/dev/null || echo "Woof cousin"')
    print("\nReady! (bye to quit)")
    while 1:
        try:
            i = input("You: ")
            if i.lower() in ["bye","quit","exit"]: break
            run(i)
        except: break
