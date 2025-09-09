# gridfs_demo.py
from pymongo import MongoClient
import gridfs
from PIL import Image
import matplotlib.pyplot as plt
import io
import os
from bson import ObjectId

# -----------------------------
# Connect to the same DB used by run.py
# -----------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["llm_app"]
fs = gridfs.GridFS(db)

def put_image_from_path(path: str, filename: str = None, content_type: str = None) -> str:
    if not filename:
        filename = os.path.basename(path)
    if not content_type:
        ext = os.path.splitext(filename)[1].lower()
        content_type = {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp"
        }.get(ext, "application/octet-stream")
    with open(path, "rb") as f:
        data = f.read()
    _id = fs.put(data, filename=filename, content_type=content_type, metadata={"source": "gridfs_demo"})
    print(f"Stored '{filename}' → GridFS _id={_id}")
    return str(_id)

def list_images():
    print("\n📁 Images in GridFS:")
    files = list(fs.find())
    for f in files:
        print(f"  - {f._id} | {f.filename} | {f.length} bytes | {f.upload_date}")
    return files

def save_from_gridfs(file_id: str, out_path: str):
    grid_out = fs.get(ObjectId(file_id))
    with open(out_path, "wb") as o:
        o.write(grid_out.read())
    print(f"Saved GridFS({file_id}) → {out_path}")

def display_from_gridfs_by_filename(filename: str):
    grid_out = fs.find_one({"filename": filename})
    if not grid_out:
        print(f"Not found: {filename}")
        return False
    img = Image.open(io.BytesIO(grid_out.read()))
    plt.figure(figsize=(8, 6))
    plt.imshow(img)
    plt.axis("off")
    plt.title(f"GridFS: {filename}")
    plt.tight_layout()
    plt.show()
    return True

def display_from_gridfs_by_id(file_id: str):
    grid_out = fs.get(ObjectId(file_id))
    img = Image.open(io.BytesIO(grid_out.read()))
    plt.figure(figsize=(8, 6))
    plt.imshow(img)
    plt.axis("off")
    plt.title(f"GridFS id: {file_id}")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # --- Demo usage ---
    # 1) (optional) store a local file into GridFS
    image_folder = "C:/Users/capta/Documents/project/"
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

    for fname in image_files:
        full_path = os.path.join(image_folder, fname)
        gid = put_image_from_path(full_path)
        print(f"✅ Stored {fname} with GridFS ID: {gid}")

    # 2) List everything that exists already (including what run.py stored)
    files = list_images()

    # 3) Try displaying the first by filename if any
    if files:
        first_name = files[0].filename
        display_from_gridfs_by_filename(first_name)

    client.close()
