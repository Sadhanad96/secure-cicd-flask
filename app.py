from flask import Flask, render_template, request
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    flake8_output = ""
    bandit_output = ""
    uploaded_filename = None  # <-- add this

    if request.method == "POST":
        file = request.files.get("file")
        if file:
            uploaded_filename = file.filename  # <-- track filename
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Run Flake8
            result = subprocess.run(["flake8", filepath], capture_output=True, text=True)
            flake8_output = result.stdout or "No issues found"

            # Run Bandit
            result = subprocess.run(["bandit", "-r", filepath], capture_output=True, text=True)
            bandit_output = result.stdout or "No issues found"

    # Pass uploaded_filename to template
    return render_template(
        "index.html",
        flake8_output=flake8_output,
        bandit_output=bandit_output,
        uploaded_filename=uploaded_filename
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
