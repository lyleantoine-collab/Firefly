```python
# agents/device_wrapper.py
import subprocess

class DeviceWrapper:
    def speak(self, text: str):
        escaped = text.replace('"', '\\"')
        subprocess.run(f'termux-tts-speak "{escaped}"', shell=True)

    def open_app(self, app: str):
        subprocess.run(f'termux-open --app {app}', shell=True)

    def type_text(self, text: str):
        escaped = text.replace('"', '\\"')
        subprocess.run(f'termux-clipboard-set "{escaped}" && termux-input-keyevent KEYCODE_PASTE', shell=True)

    def click(self, x: int, y: int):
        subprocess.run(f'termux-input tap {x} {y}', shell=True)
