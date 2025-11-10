```python
# agents/reflection_wrapper.py
import yaml
from pathlib import Path
from datetime import date

class ReflectionWrapper:
    def __init__(self):
        self.file = Path(__file__).parent.parent / "reflection" / "daily_growth.yaml"
        self.file.parent.mkdir(exist_ok=True)
        self.today = date.today().isoformat()
        self.data = self._load()

    def _load(self):
        if self.file.exists():
            with open(self.file, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}

    def _save(self):
        with open(self.file, 'w') as f:
            yaml.dump(self.data, f, default_flow_style=False)

    def get_today(self):
        return self.data.get(self.today, {})

    def save_reflection(self, learned: str, improve: str, habit: str):
        self.data[self.today] = {
            "date": self.today,
            "learned": learned.strip(),
            "improve": improve.strip(),
            "habit": habit.strip()
        }
        self._save()
