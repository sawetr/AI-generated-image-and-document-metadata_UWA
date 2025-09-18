# app.py
from flask import Flask, render_template, request, send_file, jsonify
import os
import uuid
import csv
import requests
import pandas as pd
import json
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler
from pymongo import MongoClient
from datetime import datetime
import base64


# ----------------- Basic settings -----------------
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
BATCH_SIZE = 10

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# ----------------- model path -----------------
#gemma-3-12b-it-Q4_K_M.gguf
MODEL_PATH = r"C:\Users\capta\.lmstudio\models\lmstudio-community\gemma-3-12b-it-GGUF\gemma-3-12b-it-Q4_K_M.gguf"
MMPROJ_PATH = r"C:\Users\capta\.lmstudio\models\lmstudio-community\gemma-3-12b-it-GGUF\mmproj-model-f16.gguf"


chat_handler = Llava15ChatHandler(clip_model_path=MMPROJ_PATH, verbose=False)
llm = Llama(
    model_path=MODEL_PATH,
    chat_handler=chat_handler,
    n_ctx=8194,
    n_gpu_layers=-1,
    verbose=False
)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["llm_app"]
results_collection = db["json_results"]
images_collection = db["image_link"]

# --- Helper Function to Encode Image ---
def image_to_base64_data_uri(file_path):
    """Reads an image file and converts it to a base64 data URI."""
    with open(file_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded_string}"
    
def generate_metadata(image_path):
    """
    External API call: Input image_path, return JSON dictionary
    """
    image_uri = image_to_base64_data_uri(image_path)
    system_prompt = """
    You are an expert document analyst AI. Your task is to extract structured metadata from the document image provided.
    The metadata must be in a valid JSON format and include: "author", "date" (in YYYY-MM-DD format), "Title" you can create one if you can't find any, a one-sentence "summary", and the "document_type".
    If a value cannot be found, use "Unknown".
    Output ONLY the raw JSON object, without any other text or markdown.
    """
    user_prompt = "Please analyze this document image and extract its metadata."
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image_uri}},
                {"type": "text", "text": user_prompt},
            ],
        },
    ]
 
    # The response is enforced to be JSON only
    response = llm.create_chat_completion(
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.1
    )
    raw_json = response['choices'][0]['message']['content']
    metadata = json.loads(raw_json)
    return metadata

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

        images_collection.insert_one({
            "job_id": job_id,
            "filename": filename,
        })

    batches = [saved_paths[i:i+BATCH_SIZE] for i in range(0, len(saved_paths), BATCH_SIZE)]
    return batches, job_dir


def fetch_image_paths(job_id: str):
    # Only fetch files from this job
    docs = images_collection.find({"job_id": job_id}, {"_id": 0, "filename": 1})
    return [os.path.join(UPLOAD_FOLDER, job_id, doc["filename"]) for doc in docs]

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
        return render_template('index.html', error="No files selected.")

    # 1) prepare job_id and save files in MongoDB
    job_id = uuid.uuid4().hex
    save_batches(uploaded_files, job_id)  # saves files + inserts filenames in DB

    # 2) fetch back image paths from DB
    image_paths = fetch_image_paths(job_id)

    # re-split into batches of BATCH_SIZE
    batches = [image_paths[i:i+BATCH_SIZE] for i in range(0, len(image_paths), BATCH_SIZE)]
    
    results = []
    for batch_idx, batch in enumerate(batches, start=1):
        print(f"Processing batch {batch_idx} ({len(batch)} images)")
        for image_path in batch:
            file_name = os.path.basename(image_path)
            try:
                metadata = call_ai_model(image_path)
            except Exception as e:
                metadata = {"error": f"AI call failed: {e}"}

            results.append({
                "filename": file_name,
                "author": metadata.get("author"),
                "Title": metadata.get("Title"),
                "date": metadata.get("date"),
                "summary": metadata.get("summary"),
                "document_type": metadata.get("document_type")
            })

    # 3) persist results (CSV + JSON)
    df = pd.DataFrame(results)
    csv_name, json_name = f"{job_id}.csv", f"{job_id}.json"
    csv_path, json_path = os.path.join(RESULTS_FOLDER, csv_name), os.path.join(RESULTS_FOLDER, json_name)
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2)

    results_collection.insert_one({
        "job_id": job_id,
        "created_at": datetime.utcnow().isoformat(),
        "results": results
    })

    # 4) render results page
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
    doc = results_collection.find_one({"job_id": job_id}, {"_id": 0})
    if not doc:
        return jsonify({"error": "not found"}), 404
    return jsonify(doc)

@app.route('/download/<job_id>.csv')
def download_csv(job_id):
    doc = results_collection.find_one({"job_id": job_id}, {"_id": 0})
    if not doc:
        return jsonify({"error": "not found"}), 404

    df = pd.DataFrame(doc["results"])
    csv_path = os.path.join(RESULTS_FOLDER, f"{job_id}.csv")
    df.to_csv(csv_path, index=False)

    return send_file(csv_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)
