# run.py
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, abort
from pymongo import MongoClient
from datetime import datetime, timezone
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename
import numpy as np
import os

# --- Flask setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# --- Mongo ---
client = MongoClient("mongodb://localhost:27017/")
db = client["llm_app"]
conversations = db["conversations"]

ALLOWED = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

def _score_horizontal_text(im: Image.Image) -> float:
    """
    Heuristic: higher score means 'text looks horizontal'.
    - grayscale, downscale for speed
    - binarize by mean threshold
    - row variance minus a fraction of column variance
    """
    max_w = 800
    w, h = im.size
    if w > max_w:
        im = im.resize((max_w, int(h * max_w / w)), Image.BILINEAR)

    g = im.convert("L")
    arr = np.asarray(g, dtype=np.float32)
    thr = arr.mean()
    binz = (arr < thr).astype(np.float32)  # dark (ink) ≈ 1

    row_var = binz.sum(axis=1).var()
    col_var = binz.sum(axis=0).var()
    return float(row_var - 0.5 * col_var)

def normalize_rotation(path, fallback="auto"):
    """
    Normalize orientation:
      1) Apply EXIF transpose if present.
      2) If fallback == 'auto' (recommended), evaluate 0/90/180/270
         with a heuristic and save the best.
      3) If fallback in {'cw','ccw','flip','none'}, apply that fixed rotation.
    Saves the corrected image back to the same file.
    """
    with Image.open(path) as base:
        # Step 1: EXIF
        try:
            img = ImageOps.exif_transpose(base)
        except Exception:
            img = base

        # Fixed path?
        if fallback in {"cw", "ccw", "flip", "none"}:
            if fallback == "cw":
                img = img.rotate(-90, expand=True)
            elif fallback == "ccw":
                img = img.rotate(90, expand=True)
            elif fallback == "flip":
                img = img.rotate(180, expand=True)
            img.save(path)
            return

        # Step 2: auto pick best angle
        candidates = [
            (0,   img),
            (90,  img.rotate(90,  expand=True)),
            (180, img.rotate(180, expand=True)),
            (270, img.rotate(270, expand=True)),
        ]
        best = max(candidates, key=lambda t: _score_horizontal_text(t[1]))
        best[1].save(path)


@app.route("/")
def index():
    recent = list(conversations.find({}, {"_id": 0}).sort("created_at", -1).limit(10))
    return render_template("front.html", recent=recent)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file part", 400
    f = request.files["file"]
    if not f or not f.filename:
        return "No selected file", 400

    fname = secure_filename(f.filename)
    ext = os.path.splitext(fname)[1].lower()
    if ext and ext not in ALLOWED:
        return f"Unsupported file type: {ext}", 400

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], fname)
    f.save(save_path)

    # Pick one default fallback: "cw", "ccw", "flip", or "none"
    try:
        normalize_rotation(save_path, fallback="auto")
  # change "cw" to what you need
    except Exception as e:
        print(f"[WARN] Rotation step skipped: {e}")

    now = datetime.now(timezone.utc)
    doc = {
        "type": "image_upload",
        "filename": fname,
        "status": "uploaded",
        "prompt": request.form.get("prompt") or None,
        "user_id": request.form.get("user_id") or None,
        "llm": {"provider": "lm-studio", "model": None, "response": None, "latency_ms": None},
        "created_at": now,
        "updated_at": now,
        "error": None,
    }
    conversations.insert_one(doc)
    return redirect(url_for("result", filename=fname))

@app.route("/result/<filename>")
def result(filename):
    doc = conversations.find_one({"filename": filename}, {"_id": 0})
    if not doc:
        abort(404)
    return render_template("result.html", rec=doc)

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if not os.path.isfile(file_path):
        abort(404)
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/records")
def records():
    docs = list(conversations.find({}, {"_id": 0}).sort("created_at", -1))
    return jsonify(docs)

if __name__ == "__main__":
    app.run(debug=True)


