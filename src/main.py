# src/main.py — FINAL FULL-CHAIN VERSION
import yaml
from agents.grok_wrapper import GrokWrapper
from agents.claude_wrapper import ClaudeWrapper
from agents.jan_wrapper import JanWrapper

# Load config from root (one level up)
with open('../config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def run_anthology(input_text):
    current = input_text
    print("FIREFLY ANTHOLOGY START")
    print("=" * 60)
    
    for model in config['models']:
        name = model['name']
        
        if name == 'grok':
            wrapper = GrokWrapper(model['api_key'])
        elif name == 'claude':
            wrapper = ClaudeWrapper(model['api_key'])
        elif name == 'jan':
            wrapper = JanWrapper(model.get('model_name', 'llama3'))
        else:
            print(f"Skipping unknown model: {name}")
            continue

        response = wrapper.call(current)
        print(f"{name.upper()} → {response}\n")
        current = response  # chain to next model

    print("=" * 60)
    print("FIREFLY ANTHOLOGY COMPLETE\n")
    return current

# Test run
if __name__ == "__main__":
    test_prompt = "Explain quantum computing like I'm a curious 10-year-old."
    run_anthology(test_prompt)
