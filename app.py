# app.py
from flask import Flask, render_template, request, send_file, jsonify
import os
import uuid
import csv
import requests
import pandas as pd
from model import generate_metadata

# ----------------- Basic settings -----------------
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
BATCH_SIZE = 10

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# ----------------- Link to the AI model (LM Studio/OpenAI-compatible) -----------------
def call_ai_model(image_path: str):
    """Call the local VLLM model and return the metadata dictionary."""
    try:
        return generate_metadata(image_path)
    except Exception as e:
        return {"error": str(e)}

 # expected to be JSON-like dict

# ----------------- Save uploads & make batches -----------------
def save_batches(files, job_id: str):
    """
    Save all uploaded files under uploads/<job_id>/ and return a list of batches,
    where each batch is a list of absolute file paths (size <= BATCH_SIZE).
    """
    job_dir = os.path.join(UPLOAD_FOLDER, job_id)
    os.makedirs(job_dir, exist_ok=True)

    saved_paths = []
    for f in files:
        if not f or not getattr(f, "filename", ""):
            continue
        filename = f"{uuid.uuid4()}_{f.filename}"
        path = os.path.join(job_dir, filename)
        f.save(path)  # save to disk
        saved_paths.append(path)

    # split into batches of BATCH_SIZE
    batches = [saved_paths[i:i+BATCH_SIZE] for i in range(0, len(saved_paths), BATCH_SIZE)]
    return batches, job_dir

# ----------------- Pages -----------------
@app.route('/')
def index():
    # render upload form
    return render_template('index.html')

# Frontend Upload → Backend processing (batching + AI)
@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("files")  # <input name="files" multiple>
    if not uploaded_files:
        # keep the UX same: go back to index with a message or just render empty
        return render_template('index.html', error="No files selected.")

    # 1) prepare job_id and save files in batches
    job_id = uuid.uuid4().hex
    batches, job_dir = save_batches(uploaded_files, job_id)

    # 2) loop through every image and call AI (you can swap to a mock if AI is not ready)
    results = []
    for batch_idx, batch in enumerate(batches, start=1):
        for image_path in batch:
            file_name = os.path.basename(image_path)
            try:
                metadata = call_ai_model(image_path)   # ← link to LM Studio here
            except Exception as e:
                # keep going even if one image fails
                metadata = {"error": f"AI call failed: {e}"}

            results.append({
                "filename": file_name,      # keep column names friendly for the results table
                "batch": batch_idx,
                "metadata": metadata
            })

    # 3) persist results (CSV + JSON) under results/ with job_id for download
    df = pd.DataFrame(results)
    csv_name = f"{job_id}_results.csv"
    json_name = f"{job_id}_results.json"
    csv_path = os.path.join(RESULTS_FOLDER, csv_name)
    json_path = os.path.join(RESULTS_FOLDER, json_name)
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2)

    # 4) render results page with table and download links
    return render_template(
        'results.html',
        job_id=job_id,
        results=results,
        table=df.to_html(classes="table table-striped", index=False),
        csv_file=csv_name,
        json_file=json_name
    )

# Download endpoint (CSV/JSON)
@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(RESULTS_FOLDER, filename)
    if not os.path.exists(path):
        return jsonify({"error": "file not found"}), 404
    return send_file(path, as_attachment=True)

# Optional: quick API to fetch raw JSON (if frontend needs)
@app.route('/api/jobs/<job_id>/results.json')
def api_results_json(job_id):
    json_name = f"{job_id}_results.json"
    path = os.path.join(RESULTS_FOLDER, json_name)
    if not os.path.exists(path):
        return jsonify({"error": "not found"}), 404
    return send_file(path, mimetype="application/json")

if __name__ == '__main__':
    # default port 5000 to match your teammate's habit
    app.run(debug=True, port=5001)
