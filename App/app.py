import json
from flask import Flask, render_template, request, abort
from main import run_backtest
app = Flask(__name__)

ALLOWED_IPS = {"77.90.72.145","77.99.72.145"}

@app.before_request
def whitelist():
    if request.remote_addr not in ALLOWED_IPS:
        abort(403)

@app.route("/settings", methods=["GET","POST"])
def settings():
    if request.method == "POST":
        with open("config.json","w") as f:
            json.dump({"api_key": request.form["api_key"],"api_secret": request.form["api_secret"]},f)
        return "saved"
    if request.method == "GET":
        try:
            with open("config.json") as f:
                config = json.load(f)
            return config["api_key","api_secret"]
        except FileNotFoundError:
            return ""

@app.route("/")
def index():
    final_value, buyhold_value, history, buyhold_history, dates = run_backtest()
    return render_template("index.html", final_value=final_value, buyhold_value=buyhold_value, history=history, buyhold_history=buyhold_history, dates=dates)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)