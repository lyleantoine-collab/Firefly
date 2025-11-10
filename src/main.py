import yaml
from agents.grok_wrapper import GrokWrapper

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def run_anthology(input_text):
    models = config['models']
    for model in models:
        if model['name'] == 'grok':
            wrapper = GrokWrapper(model['api_key'])
            response = wrapper.call(input_text)
            print(f"Grok says: {response}")
            input_text = response  # Chain output to next model
    return input_text
