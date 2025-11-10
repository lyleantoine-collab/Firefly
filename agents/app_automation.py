```python
# agents/app_automation.py — FIREFLY CAN USE APPS LIKE A HUMAN
import subprocess
import time
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class AppAutomation:
    def __init__(self):
        self.screenshot_path = "/sdcard/firefly_screenshot.png"
        self.ocr_model = "whisper"  # Ollama Whisper can do OCR on images too

    def open_app(self, app_name: str):
        subprocess.run(f"termux-open --app {app_name}", shell=True)
        time.sleep(2)
        logger.info(f"Opened app: {app_name}")

    def screenshot(self):
        subprocess.run("termux-screenshot -f /sdcard/firefly_screenshot.png", shell=True)
        time.sleep(1)

    def ocr(self) -> str:
        from agents.ollama_wrapper import OllamaWrapper
        ollama = OllamaWrapper("whisper")
        result = ollama.call(f"describe image {self.screenshot_path}")
        return result

    def tap_text(self, text: str):
        # Simple: find text in last OCR and tap center
        screen_text = self.ocr()
        if text.lower() in screen_text.lower():
            # Estimate center of screen
            subprocess.run("termux-input tap 540 1200", shell=True)
            logger.info(f"Tapped near: {text}")
            return True
        return False

    def type_text(self, text: str):
        subprocess.run(f'termux-clipboard-set "{text}" && termux-input-keyevent KEYCODE_PASTE', shell=True)

    def automate_task(self, task: str):
        """AI decides how to complete any task in any app"""
        from src.main import run_anthology
        steps = run_anthology(f"Break this into 5 tiny steps: {task}").split("\n")
        for step in steps:
            if not step.strip(): continue
            print(f"STEP: {step}")
            # Let Firefly decide what to do
            action = run_anthology(f"What should I do now to: {step}").lower()
            if "open" in action:
                app = action.split("open")[-1].strip()
                self.open_app(app)
            elif "type" in action or "enter" in action:
                text = action.split("type")[-1].split("enter")[-1].strip()
                self.type_text(text)
            elif "tap" in action or "click" in action:
                target = action.split("tap")[-1].split("click")[-1].strip()
                self.screenshot()
                self.tap_text(target)
            time.sleep(3)
        return "Task complete, cousin. Woof."
