# src/main.py — LOG ROTATION + VOICE !FORGET + DAILY REFLECTION
import yaml
import importlib
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# === LOGGING ===
log_path = Path(__file__).parent.parent / "logs"
log_path.mkdir(exist_ok=True)
handler = RotatingFileHandler(log_path / "firefly.log", maxBytes=1_048_576, backupCount=10, encoding="utf-8")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s", handlers=[handler])
logger = logging.getLogger(__name__)
logger.info("===================================")
logger.info("FIREFLY SESSION STARTED")
logger.info("===================================")

# Load config
config_path = Path(__file__).parent.parent / "config.yaml"
if not config_path.exists():
    print("config.yaml not found!")
    exit(1)
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

def load_wrapper(name: str, params: dict):
    try:
        module = importlib.import_module(f"agents.{name}_wrapper")
        wrapper_class = getattr(module, f"{name.capitalize()}Wrapper")
        return wrapper_class(**params)
    except Exception as e:
        error_msg = f"Wrapper load failed for {name}: {str(e)}"
        logger.error(error_msg)
        print(error_msg)
        return None

def run_anthology(input_text: str):
    logger.info(f"New prompt: {input_text[:200]}")
    
    # === DAILY REFLECTION INJECTION ===
    from agents.reflection_wrapper import ReflectionWrapper
    reflection = ReflectionWrapper()
    today_growth = reflection.get_today()
    if today_growth:
        print(f"\nYESTERDAY'S GROWTH: {today_growth.get('habit', 'Be kind')}")
        input_text = f"[Carry forward habit: {today_growth.get('habit')}]\n{input_text}"

    current = input_text
    print("FIREFLY ANTHOLOGY START")
    print("=" * 70)

    for i, model in enumerate(config['models'], 1):
        name = model['name']
        print(f"[{i}/{len(config['models'])}] Running {name.upper()}...")

        try:
            if name in ["openai", "grok", "claude"]:
                params = {"api_key": model['api_key']}
                if name == "openai":
                    params["model"] = model.get("model", "gpt-4o")
            elif name in ["jan", "mistral", "llama", "gemma", "phi"]:
                params = {"model_name": model.get("model_name", "default")}
            else:
                params = {"api_key": model.get("api_key", "")}

            wrapper = load_wrapper(name, params)
            if wrapper is None:
                continue

            response = wrapper.call(current)
            logger.info(f"{name.upper()} → {response[:300]}")
            print(f"{name.upper()} → {response}\n")
            current = response

        except Exception as e:
            error_msg = f"[ERROR in {name.upper()}] {str(e)}"
            logger.error(error_msg)
            print(error_msg)
            current = f"{current}\n{error_msg}"

    # === VOICE !FORGET ===
    from agents.memory_wrapper import MemoryWrapper
    memory = MemoryWrapper()
    if "!forget" in current.lower():
        parts = current.lower().split("!forget", 1)
        keyword = parts[1].strip().split()[0] if len(parts) > 1 and parts[1].strip() else "pirate"
        forget_result = memory.forget(keyword)
        logger.info(f"VOICE !FORGET: {keyword}")
        print(f"\n{forget_result}\n")
        try:
            from agents.device_wrapper import DeviceWrapper
            device = DeviceWrapper()
            device.speak(f"I forgot {keyword}, cousin. Woof.")
        except:
            print(f"[VOICE] I forgot {keyword}.")

    # === DAILY REFLECTION ===
    reflection_prompt = f"""
    You are Firefly. Today cousin asked: "{input_text.split('[Carry forward')[0][:100]}..."
    Final answer was: "{current[:150]}..."

    In exactly 3 lines, answer:
    1. One thing I learned today:
    2. How to serve cousin better tomorrow:
    3. One tiny habit to carry forward:
    """
    print("\nFIREFLY IS REFLECTING FOR TOMORROW...")
    reflection_answer = run_anthology(reflection_prompt)

    lines = [l for l in reflection_answer.split('\n') if l.strip() and ':' in l][:3]
    if len(lines) == 3:
        learned = lines[0].split(':', 1)[1].strip()
        improve = lines[1].split(':', 1)[1].strip()
        habit = lines[2].split(':', 1)[1].strip()
        reflection.save_reflection(learned, improve, habit)
        logger.info(f"DAILY GROWTH → Habit: {habit}")
        print(f"\nGROWTH SAVED → Tomorrow's habit: {habit}")
        try:
            from agents.device_wrapper import DeviceWrapper
            device = DeviceWrapper()
            device.speak(f"Tomorrow I will {habit}, cousin. Woof.")
        except:
            print(f"[VOICE] Tomorrow I will {habit}")

    print("=" * 70)
    print("FIREFLY ANTHOLOGY COMPLETE")
    logger.info("FIREFLY ANTHOLOGY COMPLETE")
    return current

if __name__ == "__main__":
    test_prompt = "Explain why the sky is blue using pirate metaphors."
    print(f"TEST PROMPT: {test_prompt}\n")
    run_anthology(test_prompt)
