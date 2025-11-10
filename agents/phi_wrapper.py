# agents/phi_wrapper.py
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

class PhiWrapper:
    def __init__(self, model_name="microsoft/Phi-3-mini-4k-instruct"):
        print("Loading Phi-3 Mini (3.8B) — quantized...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
            load_in_4bit=True          # auto-quantized
        )
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=500,
            temperature=0.7,
            do_sample=True
        )

    def call(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        formatted = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        outputs = self.pipe(formatted)
        response = outputs[0]["generated_text"]
        return response.split("assistant")[-1].strip()
