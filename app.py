# app.py (merged Ken version with progress + async) 
from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import os
import uuid
import pandas as pd
import json
import threading
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler
from pymongo import MongoClient
from datetime import datetime, timezone
import base64

# ----------------- Basic settings -----------------
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
BATCH_SIZE = 10

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# ----------------- model path -----------------
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

# ----------------- MongoDB connection -----------------
client = MongoClient("mongodb://localhost:27017/")
db = client["llm_app"]
results_collection = db["json_results"]
images_collection = db["image_link"]

# ----------------- Helper: encode image -----------------
def image_to_base64_data_uri(file_path):
    with open(file_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded_string}"

def generate_metadata(image_path):
    image_uri = image_to_base64_data_uri(image_path)
    system_prompt = """
    You are an expert document analyst AI. Your task is to extract structured metadata from the document image provided.
    The metadata must be in a valid JSON format and include: "author", "date" (in YYYY-MM-DD format), "Title" (create one if missing), a one-sentence "summary", and the "document_type".
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

    response = llm.create_chat_completion(
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.1
    )
    raw_json = response['choices'][0]['message']['content']
    return json.loads(raw_json)

def call_ai_model(image_path: str):
    try:
        return generate_metadata(image_path)
    except Exception as e:
        return {"error": str(e)}

# ----------------- File storage helpers -----------------
def save_batches(files, job_id: str):
    job_dir = os.path.join(UPLOAD_FOLDER, job_id)
    os.makedirs(job_dir, exist_ok=True)

    saved_paths = []
    for f in files:
        if not f or not getattr(f, "filename", ""):
            continue
        filename = f"{uuid.uuid4()}_{f.filename}"
        path = os.path.join(job_dir, filename)
        f.save(path)
        saved_paths.append(path)

        images_collection.insert_one({"job_id": job_id, "filename": filename})

    batches = [saved_paths[i:i+BATCH_SIZE] for i in range(0, len(saved_paths), BATCH_SIZE)]
    return batches, job_dir

def fetch_image_paths(job_id: str):
    docs = images_collection.find({"job_id": job_id}, {"_id": 0, "filename": 1})
    return [os.path.join(UPLOAD_FOLDER, job_id, doc["filename"]) for doc in docs]

# ----------------- Background processing -----------------
def process_job(job_id):
    image_paths = fetch_image_paths(job_id)
    batches = [image_paths[i:i+BATCH_SIZE] for i in range(0, len(image_paths), BATCH_SIZE)]

    results = []
    total = len(image_paths)
    completed = 0

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

            completed += 1
            db["progress"].update_one(
                {"job_id": job_id},
                {"$set": {"total": total, "completed": completed}},
                upsert=True
            )

    df = pd.DataFrame(results)
    csv_name, json_name = f"{job_id}.csv", f"{job_id}.json"
    df.to_csv(os.path.join(RESULTS_FOLDER, csv_name), index=False)
    df.to_json(os.path.join(RESULTS_FOLDER, json_name), orient="records", indent=2)

    results_collection.insert_one({
        "job_id": job_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "results": results
    })

# ----------------- Routes -----------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("files")
    if not uploaded_files:
        return render_template('index.html', error="No files selected.")

    job_id = uuid.uuid4().hex
    save_batches(uploaded_files, job_id)

    db["progress"].update_one(
        {"job_id": job_id},
        {"$set": {"total": len(uploaded_files), "completed": 0}},
        upsert=True
    )

    threading.Thread(target=process_job, args=(job_id,)).start()
    return redirect(url_for('processing', job_id=job_id))

@app.route('/processing/<job_id>')
def processing(job_id):
    doc = results_collection.find_one({"job_id": job_id}, {"_id": 0})
    if doc:
        df = pd.DataFrame(doc["results"])
        return render_template(
            'results.html',
            job_id=job_id,
            results=doc["results"],
            table=df.to_html(classes="table table-striped", index=False),
            csv_file=f"{job_id}.csv",
            json_file=f"{job_id}.json"
        )
    else:
        return render_template("ProcessingPage.html", job_id=job_id)

# ----------------- API -----------------
@app.route('/api/jobs/<job_id>/progress')
def api_progress(job_id):
    doc = db["progress"].find_one({"job_id": job_id}, {"_id": 0})
    if not doc:
        return jsonify({"total": 0, "completed": 0})
    return jsonify(doc)

@app.route('/api/jobs/<job_id>/results.json')
def api_results_json(job_id):
    doc = results_collection.find_one({"job_id": job_id}, {"_id": 0})
    if not doc:
        return jsonify({"error": "not found"}), 404
    return jsonify(doc)

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(RESULTS_FOLDER, filename)
    if not os.path.exists(path):
        return jsonify({"error": "file not found"}), 404
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)
 