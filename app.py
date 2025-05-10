import os
import subprocess
import uuid
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "LaTeX PDF Compiler API (Render)"

@app.route("/compile", methods=["POST"])
def compile_latex():
    data = request.get_json()
    tex_content = data.get("tex")

    if not tex_content:
        return jsonify({"error": "No LaTeX content provided"}), 400

    # Gera nome aleatório para evitar conflitos
    unique_id = str(uuid.uuid4())
    tex_file = f"/tmp/{unique_id}.tex"
    pdf_file = f"/tmp/{unique_id}.pdf"

    with open(tex_file, "w") as f:
        f.write(tex_content)

    try:
        # Compila com pdflatex (duas vezes para garantir TOC etc.)
        subprocess.run(
            ["pdflatex", "-output-directory=/tmp", tex_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Compilation failed", "log": e.stderr.decode()}), 500

    if not os.path.exists(pdf_file):
        return jsonify({"error": "PDF not generated"}), 500

    return send_file(pdf_file, mimetype="application/pdf", as_attachment=True, download_name="output.pdf")
