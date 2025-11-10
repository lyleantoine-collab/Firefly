import yaml
from agents.grok_wrapper import GrokWrapper
from agents.claude_wrapper import ClaudeWrapper
from agents.jan_wrapper import JanWrapper

with open('../config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def run_anthology(input_text):
    current = input_text
    for model in config['models']:
        name = model['name']
        if name == 'grok':
            wrapper = GrokWrapper(model['api_key'])
        elif name == 'claude':
            wrapper = ClaudeWrapper(model['api_key'])
        elif name == 'jan':
            wrapper = JanWrapper(model.get('model_name', 'llama3'))
        else:
            continue

        response = wrapper.call(current)
        print(f"{name.upper()} → {response}\n")
        current = response  # chain output to next model

    return current

# Test it
if __name__ == "__main__":
    test_prompt = "Explain quantum computing like I'm a curious 10-year-old."
    print("FIREFLY ANTHOLOGY START\n" + "="*50)
    run_anthology(test_prompt)
    print("="*50 + "\nDONE")
