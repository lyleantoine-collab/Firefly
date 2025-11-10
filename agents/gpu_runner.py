# agents/gpu_runner.py
import subprocess
from pathlib import Path

class GPURunner:
    def run(self, repo: str, script: str = "train.py"):
        path = Path(__file__).parent.parent / "tools" / repo
        cmd = f"python {script} --device cuda --batch_size 4"
        result = subprocess.run(cmd, shell=True, cwd=path, capture_output=True, text=True, timeout=600)
        return f"GPU RESULT:\n{result.stdout[-800:]}\n{result.stderr[-400:]}"
