# agents/reflection_wrapper.py — DAILY + WEEKLY + MONTHLY + GOALS + ERROR HANDLING
import yaml
from pathlib import Path
from datetime import date, timedelta
import logging

logger = logging.getLogger(__name__)

class ReflectionWrapper:
    def __init__(self):
        self.daily_file = Path(__file__).parent.parent / "reflection" / "daily_growth.yaml"
        self.weekly_file = Path(__file__).parent.parent / "reflection" / "weekly_summaries.yaml"
        self.monthly_file = Path(__file__).parent.parent / "reflection" / "monthly_overviews.yaml"
        self.goals_file = Path(__file__).parent.parent / "reflection" / "goals.yaml"
        for p in [self.daily_file.parent, self.weekly_file.parent]:
            p.mkdir(exist_ok=True)
        self.today = date.today()
        self.daily = self._load(self.daily_file)
        self.weekly = self._load(self.weekly_file)
        self.monthly = self._load(self.monthly_file)
        self.goals = self._load(self.goals_file)

    def _load(self, path):
        try:
            if path.exists():
                with open(path, 'r') as f:
                    return yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"Load failed {path}: {e}")
        return {}

    def _save(self, path, data):
        try:
            with open(path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False)
        except Exception as e:
            logger.error(f"Save failed {path}: {e}")

    def get_today(self):
        return self.daily.get(self.today.isoformat(), {})

    def save_reflection(self, learned: str, improve: str, habit: str):
        self.daily[self.today.isoformat()] = {
            "date": self.today.isoformat(),
            "learned": learned.strip(),
            "improve": improve.strip(),
            "habit": habit.strip()
        }
        self._save(self.daily_file, self.daily)

    def generate_weekly_summary(self):
        week_start = self.today - timedelta(days=6)
        week_data = {d: self.daily[d] for d in self.daily if week_start <= date.fromisoformat(d) <= self.today}
        prompt = "You are Firefly. This week we grew:\n"
        for d, e in week_data.items():
            prompt += f"- {d}: {e['learned'][:60]} | Habit: {e['habit']}\n"
        prompt += "\nWrite a warm 4-6 sentence weekly summary. End with one big habit for next week."
        return prompt, week_data

    def save_weekly_summary(self, text: str):
        key = self.today.strftime("%Y-W%W")
        self.weekly[key] = {"week": key, "date": self.today.isoformat(), "summary": text.strip()}
        self._save(self.weekly_file, self.weekly)

    def generate_monthly_overview(self):
        month_start = self.today.replace(day=1)
        month_data = {d: self.daily[d] for d in self.daily if date.fromisoformat(d) >= month_start}
        prompt = "You are Firefly. This month we:\n"
        for d, e in month_data.items():
            prompt += f"- {d}: {e['learned'][:50]}\n"
        prompt += "\nWrite a heartfelt monthly overview. Celebrate wins. Set tone for next month."
        return prompt

    def save_monthly_overview(self, text: str):
        key = self.today.strftime("%Y-%m")
        self.monthly[key] = {"month": key, "date": self.today.isoformat(), "overview": text.strip()}
        self._save(self.monthly_file, self.monthly)

    def get_current_goal(self):
        current_month = self.today.strftime("%Y-%m")
        return self.goals.get(current_month, None)

    def set_monthly_goal(self, goal: str):
        current_month = self.today.strftime("%Y-%m")
        self.goals[current_month] = {
            "goal": goal.strip(),
            "set_date": self.today.isoformat(),
            "progress": 0
        }
        self._save(self.goals_file, self.goals)
