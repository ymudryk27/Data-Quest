from __future__ import annotations
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
import json
import time

from challenges.registry import get_challenges, get_challenge
from evaluator import evaluate_solution

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"

PROGRESS_FILE = Path("storage/progress.json")
PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
if not PROGRESS_FILE.exists():
    PROGRESS_FILE.write_text(json.dumps({"cleared": [], "best_times": {}}, indent=2))


def load_progress():
    return json.loads(PROGRESS_FILE.read_text())


def save_progress(data):
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


@app.get("/")
def index():
    items = get_challenges()
    prog = load_progress()
    return render_template("index.html", challenges=items, prog=prog)


@app.get("/challenge/<cid>")
def challenge_page(cid: str):
    ch = get_challenge(cid)
    if not ch:
        flash("Challenge not found.", "error")
        return redirect(url_for("index"))
    return render_template("challenge.html", ch=ch)


@app.post("/submit/<cid>")
def submit(cid: str):
    ch = get_challenge(cid)
    if not ch:
        flash("Challenge not found.", "error")
        return redirect(url_for("index"))

    code = request.form.get("code", "")
    start = time.time()
    ok, report = evaluate_solution(code, ch)
    duration = time.time() - start

    prog = load_progress()
    if ok:
        if cid not in prog["cleared"]:
            prog["cleared"].append(cid)
        best = prog["best_times"].get(cid)
        if best is None or duration < best:
            prog["best_times"][cid] = round(duration, 3)
        save_progress(prog)
        flash("All tests passed!", "success")
    else:
        flash("Tests failed. See details below.", "warning")

    return render_template("result.html", ch=ch, ok=ok, report=report, duration=duration)


if __name__ == "__main__":
    app.run(debug=True)