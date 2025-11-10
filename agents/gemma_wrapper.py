# agents/gemma_wrapper.py  ← NEW FILE
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

class GemmaWrapper:
    def __init__(self, model_name="google/gemma-2-2b-it"):
        print("Loading Gemma 2 2B...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=torch.float16, device_map="auto"
        )
        self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer,
                            max_new_tokens=500)

    def call(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=500)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).split(prompt)[-1].strip()
