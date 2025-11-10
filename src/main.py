```python
# src/main.py — FULLY UPGRADED WITH LOGGING
import yaml
import importlib
import logging
from pathlib import Path

# === LOGGING SETUP ===
log_path = Path(__file__).parent.parent / "logs"
log_path.mkdir(exist_ok=True)

logging.basicConfig(
    filename=log_path / "firefly.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filemode="a"
)
logger = logging.getLogger(__name__)

logger.info("===================================")
logger.info("FIREFLY SESSION STARTED")
logger.info("===================================")

# Load config from root
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
            elif name in ["jan", "mistral", "llama"]:
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

    print("=" * 70)
    print("FIREFLY ANTHOLOGY COMPLETE")
    logger.info("FIREFLY ANTHOLOGY COMPLETE")
    logger.info(f"Final answer length: {len(current)} characters")
    
    return current

if __name__ == "__main__":
    test_prompt = "Explain why the sky is blue using only pirate metaphors."
    print(f"TEST PROMPT: {test_prompt}\n")
    run_anthology(test_prompt)
