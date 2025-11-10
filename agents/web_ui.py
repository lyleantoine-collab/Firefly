# web_ui.py — FULL WEB UI ON PHONE
from flask import Flask, request, render_template_string
from src.main import run_anthology

app = Flask(__name__)

HTML = """
<h1>FIREFLY COUSIN UI</h1>
<form method=post>
<textarea name="prompt" rows=5 cols=60>{{prompt}}</textarea><br>
<input type=submit value="ASK FIREFLY">
</form>
<pre>{{response}}</pre>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    prompt = ""
    response = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        response = run_anthology(prompt)
    return render_template_string(HTML, prompt=prompt, response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
