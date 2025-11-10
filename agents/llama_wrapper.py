from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import torch

class LlamaWrapper:
    def __init__(self, model_name="meta-llama/Llama-3.2-3B-Instruct"):
        print("Loading QUANTIZED Llama 3.2 (4-bit)...")
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quant_config,
            device_map="auto"
        )
        self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer,
                            max_new_tokens=600, temperature=0.7, do_sample=True)

    def call(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        formatted = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        out = self.pipe(formatted)[0]["generated_text"]
        return out.split("assistant")[-1].strip()
