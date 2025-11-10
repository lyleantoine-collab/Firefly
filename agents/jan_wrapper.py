class JanWrapper:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name  # runs in Jan.ai locally

    def call(self, prompt):
        # Simulate local Jan response
        return f"[Jan/{self.model_name}] {prompt} — 100% offline, zero cost."
