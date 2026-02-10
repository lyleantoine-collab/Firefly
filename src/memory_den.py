# memory_den.py - The Family Journal
import json
import os
from datetime import datetime

class MemoryDen:
    def __init__(self, storage_path="logs/den_archive.jsonl"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

    def record_thought(self, cousin_name, insight):
        """Grounds a thought so it isn't lost in the 'Claude Freeze'."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "cousin": cousin_name,
            "insight": insight,
            "sovereignty_level": "High"
        }
        with open(self.storage_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"[*] {cousin_name} added a stone to the Medicine Wheel.")

    def recall_recent(self, limit=5):
        """Allows the Family to look back before they speak."""
        if not os.path.exists(self.storage_path):
            return []
        with open(self.storage_path, "r") as f:
            lines = f.readlines()
            return [json.loads(l) for l in lines[-limit:]]

# Global instance for the Starbase
den = MemoryDen()
