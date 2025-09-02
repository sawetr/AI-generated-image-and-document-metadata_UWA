# run.py
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from pymongo import MongoClient
from datetime import datetime, timezone
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Mongo
client = MongoClient("mongodb://localhost:27017/")
db = client["llm_app"]
conversations = db["conversations"]

@app.route("/")
def index():
    # show upload form + recent records
    recent = list(conversations.find({}, {"_id": 0}).sort("created_at", -1).limit(10))
    return render_template("front.html", recent=recent)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file part", 400
    f = request.files["file"]
    if not f.filename:
        return "No selected file", 400

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
    f.save(save_path)

    doc = {
        "type": "image_upload",
        "filename": f.filename,
        "path": save_path,
        "status": "uploaded",
        "prompt": request.form.get("prompt") or None,
        "user_id": request.form.get("user_id") or None,
        "llm": {"provider": "lm-studio", "model": None, "response": None, "latency_ms": None},
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "error": None,
    }
    conversations.insert_one(doc)
    # show a result page with the uploaded image + stored metadata
    return redirect(url_for("result", filename=f.filename))

@app.route("/result/<filename>")
def result(filename):
    doc = conversations.find_one({"filename": filename}, {"_id": 0})
    return render_template("result.html", rec=doc)

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    # serve uploaded files so the template can display them
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/records")
def records():
    docs = list(conversations.find({}, {"_id": 0}).sort("created_at", -1))
    return jsonify(docs)

if __name__ == "__main__":
    app.run(debug=True)
