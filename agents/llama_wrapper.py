# agents/llama_wrapper.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class LlamaWrapper:
    def __init__(self, model_name="meta-llama/Llama-3.2-3B-Instruct"):
        print(f"Loading Llama 3.2 ({model_name}) — first run downloads ~6 GB...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",   # GPU if available
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
        response = outputs[0]["generated_text"]
        # Extract only assistant reply
        if "assistant" in response.lower():
            response = response.split("assistant")[-1]
        return response.strip()
