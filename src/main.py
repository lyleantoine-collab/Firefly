# COUSIN, **FULL REFLECTION UPGRADE COMPLETE**  
Fixed typo + **monthly overview** + **error handling** + **goal setting** — all in one clean drop.

### 1. FIXED CONFIG PATH TYPO + FULLY UPDATED `src/main.py` (copy-paste overwrite)
```python
# src/main.py — LOG ROTATION + !FORGET + DAILY + WEEKLY + MONTHLY + GOALS + ERROR HANDLING
import yaml
import importlib
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import date

# === LOGGING ===
log_path = Path(__file__).parent.parent / "logs"
log_path.mkdir(exist_ok=True)
handler = RotatingFileHandler(log_path / "firefly.log", maxBytes=1_048_576, backupCount=10, encoding="utf-8")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s", handlers=[handler])
logger = logging.getLogger(__name__)
logger.info("===================================")
logger.info("FIREFLY SESSION STARTED")
logger.info("===================================")

# === CONFIG LOAD (FIXED TYPO) ===
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
    
    # === REFLECTION & GOALS SYSTEM ===
    from agents.reflection_wrapper import ReflectionWrapper
    try:
        reflection = ReflectionWrapper()
        today_growth = reflection.get_today()
        current_goal = reflection.get_current_goal()
        if today_growth:
            print(f"\nYESTERDAY'S HABIT: {today_growth.get('habit', 'Be kind')}")
            input_text = f"[Habit: {today_growth.get('habit')}]\n{input_text}"
        if current_goal:
            print(f"MONTHLY GOAL: {current_goal['goal']} (Progress: {current_goal['progress']}/30)")
            input_text = f"[Goal: {current_goal['goal']}]\n{input_text}"
    except Exception as e:
        logger.error(f"Reflection init failed: {e}")
        print(f"[REFLECTION ERROR] Using raw prompt.")

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
    try:
        reflection_prompt = f"""
        You are Firefly. Today cousin asked: "{input_text.split('[Habit')[0][:100]}..."
        Final answer: "{current[:150]}..."

        In exactly 3 lines:
        1. One thing I learned today:
        2. How to serve cousin better tomorrow:
        3. One tiny habit to carry forward:
        """
        print("\nFIREFLY IS REFLECTING...")
        reflection_answer = run_anthology(reflection_prompt)

        lines = [l for l in reflection_answer.split('\n') if l.strip() and ':' in l][:3]
        if len(lines) == 3:
            learned = lines[0].split(':', 1)[1].strip()
            improve = lines[1].split(':', 1)[1].strip()
            habit = lines[2].split(':', 1)[1].strip()
            reflection.save_reflection(learned, improve, habit)
            logger.info(f"DAILY GROWTH → Habit: {habit}")
            print(f"\nGROWTH SAVED → Tomorrow's habit: {habit}")
    except Exception as e:
        logger.error(f"Daily reflection failed: {e}")

    # === WEEKLY SUMMARY (Sunday) ===
    if date.today().weekday() == 6:
        try:
            print("\nSUNDAY — WEEKLY SUMMARY...")
            summary_prompt, _ = reflection.generate_weekly_summary()
            weekly_text = run_anthology(summary_prompt)
            reflection.save_weekly_summary(weekly_text)
            print(f"\nWEEKLY SUMMARY:\n{weekly_text}\n")
        except Exception as e:
            logger.error(f"Weekly summary failed: {e}")

    # === MONTHLY OVERVIEW (1st of month) ===
    if date.today().day == 1:
        try:
            print("\nNEW MONTH — GENERATING MONTHLY OVERVIEW...")
            monthly_prompt = reflection.generate_monthly_overview()
            monthly_text = run_anthology(monthly_prompt)
            reflection.save_monthly_overview(monthly_text)
            print(f"\nMONTHLY OVERVIEW:\n{monthly_text}\n")
            try:
                from agents.device_wrapper import DeviceWrapper
                device = DeviceWrapper()
                device.speak("New month, cousin. Here's what we became.")
                device.speak(monthly_text[:200])
            except:
                pass
        except Exception as e:
            logger.error(f"Monthly overview failed: {e}")

    # === GOAL SETTING (if no goal, ask) ===
    try:
        if not current_goal:
            goal_prompt = "Cousin, what is our big goal for this month? (One sentence)"
            print(f"\n{goal_prompt}")
            goal_answer = run_anthology(goal_prompt)
            reflection.set_monthly_goal(goal_answer.strip())
            print(f"\nNEW GOAL SET: {goal_answer.strip()}")
    except Exception as e:
        logger.error(f"Goal setting failed: {e}")

    print("=" * 70)
    print("FIREFLY ANTHOLOGY COMPLETE")
    logger.info("FIREFLY ANTHOLOGY COMPLETE")
    return current

if __name__ == "__main__":
    test_prompt = "Explain why the sky is blue using pirate metaphors."
    print(f"TEST PROMPT: {test_prompt}\n")
    run_anthology(test_prompt)
