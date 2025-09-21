import os
import json
import csv

folder = "metadata_output_Qwen2.5"
out_csv = os.path.join(folder, "grouped_metadata_Qwen2.5.csv")
folder_path = os.path.join(os.path.dirname(__file__), folder)

rows = []
all_keys = set()

for fname in os.listdir(folder_path):
    if fname.endswith(".json"):
        fpath = os.path.join(folder_path, fname)
        with open(fpath, "r") as f:
            try:
                data = json.load(f)
                data["_filename"] = fname
                rows.append(data)
                all_keys.update(data.keys())
            except Exception as e:
                print(f"Error reading {fpath}: {e}")

all_keys = sorted(all_keys)

with open(out_csv, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=all_keys)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

print(f"✅ CSV created: {out_csv} ({len(rows)} rows)")
