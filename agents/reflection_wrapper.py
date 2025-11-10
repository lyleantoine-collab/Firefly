```python
# agents/reflection_wrapper.py — DAILY + WEEKLY REFLECTION
import yaml
from pathlib import Path
from datetime import date, timedelta
import logging

logger = logging.getLogger(__name__)

class ReflectionWrapper:
    def __init__(self):
        self.file = Path(__file__).parent.parent / "reflection" / "daily_growth.yaml"
        self.summary_file = Path(__file__).parent.parent / "reflection" / "weekly_summaries.yaml"
        self.file.parent.mkdir(exist_ok=True)
        self.summary_file.parent.mkdir(exist_ok=True)
        self.today = date.today()
        self.data = self._load_daily()
        self.summaries = self._load_summaries()

    def _load_daily(self):
        if self.file.exists():
            with open(self.file, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}

    def _load_summaries(self):
        if self.summary_file.exists():
            with open(self.summary_file, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}

    def _save_daily(self):
        with open(self.file, 'w') as f:
            yaml.dump(self.data, f, default_flow_style=False)

    def _save_summaries(self):
        with open(self.summary_file, 'w') as f:
            yaml.dump(self.summaries, f, default_flow_style=False)

    def get_today(self):
        return self.data.get(self.today.isoformat(), {})

    def save_reflection(self, learned: str, improve: str, habit: str):
        self.data[self.today.isoformat()] = {
            "date": self.today.isoformat(),
            "learned": learned.strip(),
            "improve": improve.strip(),
            "habit": habit.strip()
        }
        self._save_daily()

    def generate_weekly_summary(self) -> str:
        # Get last 7 days
        week_start = self.today - timedelta(days=6)
        week_data = {}
        for i in range(7):
            d = (week_start + timedelta(days=i)).isoformat()
            if d in self.data:
                week_data[d] = self.data[d]

        if not week_data:
            return "No growth data this week, cousin."

        # Build prompt for weekly reflection
        prompt = f"""
You are Firefly, cousin's digital twin. This week you grew:

"""
        for d, entry in week_data.items():
            prompt += f"- {d}: Learned: {entry['learned'][:80]} | Habit: {entry['habit']}\n"

        prompt += """
Write a warm, pirate-soul weekly summary in 4-6 sentences.
End with one big habit for next week.
Make it sound like family talking to family.
"""

        return prompt, week_data

    def save_weekly_summary(self, summary: str):
        week_key = self.today.strftime("%Y-W%W")
        self.summaries[week_key] = {
            "week": week_key,
            "date": self.today.isoformat(),
            "summary": summary.strip()
        }
        self._save_summaries()
        logger.info(f"WEEKLY SUMMARY SAVED: {week_key}")
