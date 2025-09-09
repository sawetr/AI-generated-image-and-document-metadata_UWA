# run.py
# run.py
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, abort, make_response, send_file
from pymongo import MongoClient
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
from bson import ObjectId

import gridfs
import numpy as np
from PIL import Image, ImageOps
import io
import os

# -----------------------------
# Flask setup
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -----------------------------
# Mongo (local docker or Atlas)
# -----------------------------
# For Atlas, replace with your URI:
# client = MongoClient("mongodb+srv://<user>:<pass>@<cluster-url>/")
client = MongoClient("mongodb://localhost:27017/")
db = client["llm_app"]
conversations = db["conversations"]
fs = gridfs.GridFS(db)

ALLOWED = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

# -----------------------------
# Orientation scoring heuristic
# -----------------------------
def _score_horizontal_text(im: Image.Image) -> float:
    """
    Heuristic: higher score => image looks like it has horizontal text lines.
    Steps:
      - downscale for speed
      - grayscale
      - binarize around mean
      - variance of row sums minus fraction of column sums (prefer horizontal bands)
    """
    max_w = 800
    w, h = im.size
    if w > max_w:
        im = im.resize((max_w, int(h * max_w / w)), Image.BILINEAR)

    g = im.convert("L")
    arr = np.asarray(g, dtype=np.float32)
    thr = float(arr.mean())
    binz = (arr < thr).astype(np.float32)  # dark ink ≈ 1

    row_var = binz.sum(axis=1).var()
    col_var = binz.sum(axis=0).var()
    return float(row_var - 0.5 * col_var)

def normalize_rotation(path: str, mode: str = "auto") -> str:
    """
    Normalize orientation and overwrite the file at 'path'.

    Returns a label of what was applied:
      "exif"  -> EXIF transpose changed pixels
      "0"     -> best angle was 0 deg (no rotation)
      "90"    -> best angle was 90 deg CCW
      "180"   -> best angle was 180 deg
      "270"   -> best angle was 270 deg
      "cw"    -> forced -90 (clockwise)
      "ccw"   -> forced +90 (counter-clockwise)
      "flip"  -> forced 180
      "none"  -> no change
    """
    with Image.open(path) as base:
        # Step 1: try EXIF fix
        try:
            img = ImageOps.exif_transpose(base)
        except Exception:
            img = base

        # Fixed direction shortcut
        if mode in {"cw", "ccw", "flip", "none"}:
            label = "none"
            if mode == "cw":
                img = img.rotate(-90, expand=True); label = "cw"
            elif mode == "ccw":
                img = img.rotate(90, expand=True);  label = "ccw"
            elif mode == "flip":
                img = img.rotate(180, expand=True); label = "flip"
            # 'none' -> do nothing
            img.save(path)
            return label

        # If EXIF actually changed pixels, we can keep it; but we’ll still
        # check auto angles since some EXIF rotations can still leave it skewed.
        candidates = [
            (0,   img),
            (90,  img.rotate(90,  expand=True)),
            (180, img.rotate(180, expand=True)),
            (270, img.rotate(270, expand=True)),
        ]
        # Score each orientation
        best_angle, best_img, best_score = None, None, -1e18
        for ang, im in candidates:
            try:
                sc = _score_horizontal_text(im)
            except Exception:
                sc = -1e18
            if sc > best_score:
                best_score, best_angle, best_img = sc, ang, im

        best_img.save(path)
        if best_angle == 0:
            # Detect if EXIF did some work:
            if img.tobytes() != base.tobytes():
                return "exif"
            return "0"
        return str(best_angle)

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def index():
    recent = list(
        conversations.find({}, {"_id": 0})
        .sort("created_at", -1)
        .limit(10)
    )
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

    # Save raw, then normalize in place
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], fname)
    f.save(save_path)

    try:
        rotation_applied = normalize_rotation(save_path, mode="auto")
    except Exception as e:
        print(f"[WARN] Rotation step skipped: {e}")
        rotation_applied = "error"

    # Also store the rotated image into GridFS
    content_type_map = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp"
    }
    ctype = content_type_map.get(ext, "application/octet-stream")

    with open(save_path, "rb") as fh:
        file_bytes = fh.read()
    file_id = fs.put(
        file_bytes,
        filename=fname,
        content_type=ctype,
        metadata={"rotated": True, "source": "uploads", "rotation": rotation_applied},
    )

    now = datetime.now(timezone.utc)
    doc = {
        "type": "image_upload",
        "filename": fname,                 # disk name
        "gridfs_id": str(file_id),         # id in GridFS
        "status": "uploaded",
        "rotation": rotation_applied,      # what we applied (info only)
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
    # Tip: in result.html, prefer GridFS if gridfs_id exists:
    # <img src="{{ url_for('file_stream', file_id=rec.gridfs_id) }}?v={{ rec.updated_at.timestamp() }}">
    return render_template("result.html", rec=doc)

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if not os.path.isfile(file_path):
        abort(404)
    resp = make_response(send_from_directory(app.config["UPLOAD_FOLDER"], filename))
    # help avoid stale cache during testing
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

@app.route("/files/<file_id>")
def file_stream(file_id):
    # Stream from GridFS
    try:
        grid_out = fs.get(ObjectId(file_id))
    except Exception:
        abort(404)
    data = grid_out.read()
    return send_file(
        io.BytesIO(data),
        mimetype=grid_out.content_type or "application/octet-stream",
        download_name=grid_out.filename
    )

@app.route("/records")
def records():
    docs = list(conversations.find({}, {"_id": 0}).sort("created_at", -1))
    return jsonify(docs)

if __name__ == "__main__":
    app.run(debug=True)



