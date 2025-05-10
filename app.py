from flask import Flask, request, send_file
import os
import uuid
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "LaTeX API is running"

@app.route("/compile", methods=["POST"])
def compile_latex():
    data = request.json
    tex = data.get("tex", "")
    if not tex:
        return "Missing 'tex' content", 400

    filename = f"/tmp/{uuid.uuid4()}"
    tex_file = f"{filename}.tex"
    pdf_file = f"{filename}.pdf"

    with open(tex_file, "w") as f:
        f.write(tex)

    subprocess.run(["pdflatex", "-output-directory=/tmp", tex_file], check=True)

    return send_file(pdf_file, mimetype="application/pdf")
