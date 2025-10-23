from flask import Flask, render_template, request
import os
import subprocess
import re

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def parse_flake8(output):
    lines = []
    for line in output.splitlines():
        # Example: /path/to/file.py:3:1: F401 'os' imported but unused
        match = re.match(r".*:(\d+):\d+: (\w+) (.+)", line)
        if match:
            lines.append({
                "line": match.group(1),
                "type": match.group(2),
                "message": match.group(3)
            })
    return lines

def parse_bandit(output):
    issues = []
    blocks = output.split("--------------------------------------------------")
    for block in blocks:
        match = re.search(r"Location: .*:(\d+):", block)
        code_match = re.search(r"\[([A-Z0-9]+):.*\]", block)
        severity_match = re.search(r"Severity: (\w+)", block)
        desc_match = re.search(r"More Info: .*\n\s*(.+)", block)
        if match and code_match and severity_match:
            issues.append({
                "line": match.group(1),
                "code": code_match.group(1),
                "severity": severity_match.group(1),
                "desc": desc_match.group(1).strip() if desc_match else ""
            })
    return issues

@app.route("/", methods=["GET", "POST"])
def index():
    flake8_lines = []
    bandit_issues = []
    uploaded_filename = None

    if request.method == "POST":
        file = request.files.get("file")
        if file:
            uploaded_filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, uploaded_filename)
            file.save(filepath)

            # Run Flake8
            result = subprocess.run(["flake8", filepath], capture_output=True, text=True)
            flake8_lines = parse_flake8(result.stdout)

            # Run Bandit
            result = subprocess.run(["bandit", "-r", filepath], capture_output=True, text=True)
            bandit_issues = parse_bandit(result.stdout)

    return render_template(
        "index.html",
        uploaded_filename=uploaded_filename,
        flake8_lines=flake8_lines,
        bandit_issues=bandit_issues
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
