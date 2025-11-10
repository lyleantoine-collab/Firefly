# src/main.py — MODULAR, ROBUST, READY FOR REAL APIs
import yaml
from pathlib import Path

# Dynamic imports — only load what's in config
WRAPPERS = {
    "grok": "agents.grok_wrapper.GrokWrapper",
    "openai": "agents.openai_wrapper.OpenAIWrapper",
    "claude": "agents.claude_wrapper.ClaudeWrapper",
    "jan": "agents.jan_wrapper.JanWrapper"
}

def load_wrapper(name: str, params: dict):
    if name not in WRAPPERS:
        raise ValueError(f"Unknown model: {name}")
    
    module_path, class_name = WRAPPERS[name].rsplit(".", 1)
    module = __import__(module_path, fromlist=[class_name])
    wrapper_class = getattr(module, class_name)
    
    return wrapper_class(**params)

def run_anthology(input_text: str):
    config_path = Path(__file__).parent.parent / "config.yaml"
    if not config_path.exists():
        print("config.yaml not found!")
        return

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    current = input_text
    print("FIREFLY ANTHOLOGY START")
    print("=" * 70)

    for i, model in enumerate(config['models'], 1):
        name = model['name']
        print(f"[{i}/{len(config['models'])}] Running {name.upper()}...")

        try:
            if name == "openai":
                params = {"api_key": model['api_key'], "model": model.get("model", "gpt-4o")}
            elif name == "jan":
                params = {"model_name": model.get("model_name", "llama3")}
            else:
                params = {"api_key": model['api_key']}

            wrapper = load_wrapper(name, params)
            response = wrapper.call(current)
            print(f"{name.upper()} → {response}\n")
            current = response

        except Exception as e:
            error_msg = f"[ERROR in {name.upper()}] {str(e)}"
            print(error_msg)
            current = f"{current}\n{error_msg}"

    print("=" * 70)
    print("FIREFLY ANTHOLOGY COMPLETE")
    return current

if __name__ == "__main__":
    test = "Explain why the sky is blue using only pirate metaphors."
    run_anthology(test)
