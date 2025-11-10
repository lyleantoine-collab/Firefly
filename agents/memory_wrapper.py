```python
# agents/memory_wrapper.py
import re
from pathlib import Path

class MemoryWrapper:
    def __init__(self):
        self.log_path = Path(__file__).parent.parent / "logs" / "firefly.log"
        self.backup_path = Path(__file__).parent.parent / "logs" / "firefly.log.bak"

    def forget(self, keyword: str) -> str:
        if not self.log_path.exists():
            return "No log file found."

        # Backup current log
        if self.log_path.exists():
            self.log_path.replace(self.backup_path)

        try:
            with open(self.backup_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Filter out any line containing the keyword
            filtered = [line for line in lines if keyword.lower() not in line.lower()]

            # Overwrite log with cleaned version
            with open(self.log_path, 'w', encoding='utf-8') as f:
                f.writelines(filtered)

            removed = len(lines) - len(filtered)
            return f"FORGOT {removed} memories containing '{keyword}'. Log cleaned."
        
        except Exception as e:
            return f"Error during forget: {str(e)}"
