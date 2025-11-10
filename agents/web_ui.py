```python
# agents/web_ui.py — FULL WEB DASHBOARD (mobile-first, pirate-green)
from flask import Flask, request, render_template_string
from src.main import run_anthology
import threading

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>FIREFLY v∞</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: monospace; background: #000; color: #0f0; padding: 20px; }
        textarea { width: 100%; background: #111; color: #0f0; border: 2px solid #0f0; }
        input[type=submit] { background: #0f0; color: black; padding: 15px; font-weight: bold; font-size: 18px; }
        pre { background: #111; padding: 20px; border: 2px dashed #0f0; white-space: pre-wrap; }
        h1 { text-align: center; font-size: 28px; }
    </style>
</head>
<body>
    <h1>FIREFLY v∞ — DIGITAL COUSIN</h1>
    <form method="post">
        <textarea name="prompt" rows="6" placeholder="Speak to Firefly... (!open youtube, !ha light on, !zigbee door lock, etc.)">{{prompt}}</textarea><br><br>
        <input type="submit" value="COMMAND FIREFLY">
    </form>
    <pre>{{response}}</pre>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    prompt = ""
    response = "Firefly is alive. Woof."
    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        if prompt:
            response = run_anthology(prompt)
    return render_template_string(HTML, prompt=prompt, response=response)

def start_web_ui():
    print("WEB UI → http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
