from pymongo import MongoClient
import gridfs
from bson import ObjectId
from PIL import Image
import io

# --------------------------------------------
# Setup MongoDB
# --------------------------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["llm_app"]
fs = gridfs.GridFS(db)
conversations = db["conversations"]

# --------------------------------------------
# Dummy LLM Metadata Generator (Mock)
# --------------------------------------------
def mock_llm_generate_metadata(image_bytes):
    # In real use, call your model here
    return {
        "caption": "This is a mock caption.",
        "objects": ["mock_object_1", "mock_object_2"],
        "tags": ["mock", "metadata"]
    }

# --------------------------------------------
# Step 1: Get the batch record
# --------------------------------------------
batch = conversations.find_one({"type": "image_upload", "status": "uploaded"})

if not batch:
    print("❌ No batch found.")
    exit()

print(f"📦 Found batch: {batch['filename'] if 'filename' in batch else 'N/A'}")

# --------------------------------------------
# Step 2: Retrieve 10 images from GridFS
# --------------------------------------------
gridfs_ids = batch.get("gridfs_ids", [])

if len(gridfs_ids) != 10:
    print(f"⚠️ Expected 10 images, but got {len(gridfs_ids)}")
else:
    print("✅ 10 images found in batch.")

# --------------------------------------------
# Step 3: Process each image through the LLM
# --------------------------------------------
metadata_list = []

for file_id in gridfs_ids:
    try:
        grid_out = fs.get(ObjectId(file_id))
        image_bytes = grid_out.read()
        image = Image.open(io.BytesIO(image_bytes))  # Optional for visual check

        # Send to LLM
        metadata = mock_llm_generate_metadata(image_bytes)
        metadata_list.append({
            "gridfs_id": str(file_id),
            "filename": grid_out.filename,
            "metadata": metadata
        })

    except Exception as e:
        print(f"❌ Failed for file ID {file_id}: {e}")

# --------------------------------------------
# Step 4: Store metadata back into MongoDB
# --------------------------------------------
conversations.update_one(
    {"_id": batch["_id"]},
    {"$set": {"status": "processed", "outputs": metadata_list}}
)

print("\n✅ Metadata generation complete.")
for i, m in enumerate(metadata_list):
    print(f"\n🔹 Image {i+1}: {m['filename']}")
    print(m["metadata"])

client.close()
