from flask import Flask, render_template, request, send_file
import os
import pandas as pd
import uuid
from model import model 

#A simple Flask web app to upload multiple images/documents, process them
#(currently dummy metadata, placeholder for AI model), and display results in JSON and CSV formats with download options.

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # Load index.html (upload form)
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("files")
    results = []

    for file in uploaded_files:
        if file.filename == '':
            continue

        filename = f"{uuid.uuid4()}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # === Partner’s AI Model Placeholder ===
        # metadata = run_ai_model(filepath)
        # results.append(metadata)

        # Dummy metadata
        metadata = {
            "filename": file.filename,
            "title": "Demo Title",
            "type": "Document",
            "date": "2025-09-07",
            "summary": "This is placeholder metadata until AI model is connected."
        }
        results.append(metadata)

    # Convert results → CSV + JSON
    df = pd.DataFrame(results)
    csv_path = os.path.join(RESULTS_FOLDER, "results.csv")
    json_path = os.path.join(RESULTS_FOLDER, "results.json")
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2)

    return render_template(
        'results.html',
        results=results,
        table=df.to_html(classes="table table-striped", index=False),
        csv_file="results.csv",
        json_file="results.json"
    )

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(RESULTS_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
