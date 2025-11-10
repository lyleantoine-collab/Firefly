# agents/mistral_wrapper.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class MistralWrapper:
    def __init__(self, model_name="mistralai/Mistral-7B-Instruct-v0.3"):
        print(f"Loading Mistral ({model_name}) — this may take a minute first time...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",          # uses GPU if available
            trust_remote_code=True
        )
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=600,
            temperature=0.7,
            do_sample=True,
            top_p=0.9
        )

    def call(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        formatted = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        outputs = self.pipe(formatted)
        # Extract only assistant reply
        response = outputs[0]["generated_text"]
        if "<|assistant|>" in response:
            response = response.split("<|assistant|>")[-1]
        return response.strip()
