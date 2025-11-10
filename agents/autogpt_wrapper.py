# agents/autogpt_wrapper.py
from concurrent.futures import ThreadPoolExecutor
from src.main import run_anthology

class AutoGPTWrapper:
    def __init__(self, max_workers=3):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def spawn(self, task: str):
        future = self.executor.submit(run_anthology, task)
        return f"Spawned parallel task: {task[:50]}..."
