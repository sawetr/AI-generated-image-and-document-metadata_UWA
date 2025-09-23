import os
import pandas as pd
import chardet
from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer, util

# --- Paths ---
GROUND_TRUTH_PATH = "Client_Ground_Truth/metadata_Ground_Truth.csv"
MODEL_RESULTS_FOLDER = "Our_AI_Model_Results"
OUTPUT_FOLDER = "Validation_Reports"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# --- Load embedding model (do this once) ---
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Helpers ---
def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        raw = f.read(100000)
    result = chardet.detect(raw)
    return result["encoding"]

def normalize_date(date_str):
    """Normalize different date formats into YYYY-MM for fair comparison."""
    if pd.isna(date_str) or str(date_str).lower() == "unknown":
        return "unknown"
    try:
        return pd.to_datetime(str(date_str), errors="coerce").strftime("%Y-%m")
    except:
        return str(date_str).strip().lower()

def fuzzy_match(str1, str2, threshold=75):
    """Fuzzy string match using token sort ratio."""
    if pd.isna(str1) or pd.isna(str2):
        return False
    if str(str1).lower() == "unknown" and str(str2).lower() == "unknown":
        return True
    score = fuzz.token_sort_ratio(str(str1).lower(), str(str2).lower())
    return score >= threshold

def doc_type_match_fn(truth_val, model_val, threshold=70):
    """
    Flexible doc type match:
    - Ground truth may contain multiple valid values separated by '/' or ','
    - Model is correct if it matches ANY of them
    """
    if pd.isna(truth_val) or pd.isna(model_val):
        return False
    truth_options = [opt.strip().lower() for part in str(truth_val).split("/") for opt in part.split(",")]
    model_val = str(model_val).strip().lower()

    for truth in truth_options:
        score = fuzz.token_sort_ratio(model_val, truth)
        if score >= threshold:
            return True
    return False

def semantic_match(truth_text, model_text, threshold=0.65):
    """Embed & compare semantic similarity between two strings."""
    if pd.isna(truth_text) or pd.isna(model_text):
        return False, 0.0
    if str(truth_text).strip() == "" or str(model_text).strip() == "":
        return False, 0.0
    truth_emb = embedding_model.encode(str(truth_text), convert_to_tensor=True)
    model_emb = embedding_model.encode(str(model_text), convert_to_tensor=True)
    sim = util.cos_sim(truth_emb, model_emb).item()
    return sim >= threshold, sim

# --- Validation Logic ---
def validate_model(model_path, ground_df):
    encoding = detect_encoding(model_path)
    print(f"ℹ️ Detected encoding for {model_path}: {encoding}")
    model_df = pd.read_csv(model_path, encoding=encoding)

    # --- Normalize column names ---
    model_df.rename(columns=lambda x: x.strip().lower(), inplace=True)
    ground_df.rename(columns=lambda x: x.strip().lower(), inplace=True)

    # Explicit mapping in case models use variants
    rename_map = {
        "_filename": "filename",
        "title": "title",
        "Title": "title",
        "document_type": "document_type",
        "doc_type": "document_type",
        "summary": "summary",
        "author": "author",
        "date": "date",
    }
    model_df.rename(columns=rename_map, inplace=True)

    # Normalize filename
    if "filename" in model_df.columns:
        model_df["filename"] = model_df["filename"].str.replace("_metadata.json", "", regex=False)
    ground_df["filename"] = ground_df["filename"].str.replace(".json", "", regex=False)

    # Merge
    merged = pd.merge(model_df, ground_df, on="filename", suffixes=("_model", "_truth"))
    print(f"\n🔎 For {os.path.basename(model_path)} merged columns are:\n{list(merged.columns)}")

    results = []
    for _, row in merged.iterrows():
        # Author check
        author_match = fuzzy_match(row.get("author_model", ""), row.get("author_truth", ""))

        # Date check
        date_match = normalize_date(row.get("date_model", "")) == normalize_date(row.get("date_truth", ""))

        # Title check (semantic similarity)
        title_ok, title_score = semantic_match(row.get("title_truth", ""), row.get("title_model", ""))

        # Document type check
        doc_type_match = doc_type_match_fn(row.get("document_type_truth", ""), row.get("document_type_model", ""))

        # Summary check (semantic similarity)
        summary_ok, summary_score = semantic_match(row.get("summary_truth", ""), row.get("summary_model", ""))

        # Row-level scoring
        checks = {
            "author_match": author_match,
            "date_match": date_match,
            "title_match": title_ok,
            "summary_match": summary_ok,
            "document_type_match": doc_type_match,
        }
        row_score = sum(checks.values()) / len(checks) * 100

        results.append({
            "filename": row["filename"],

            "author_model": row.get("author_model", ""),
            "author_truth": row.get("author_truth", ""),
            "author_match": "✅" if author_match else "❌",

            "date_model": row.get("date_model", ""),
            "date_truth": row.get("date_truth", ""),
            "date_match": "✅" if date_match else "❌",

            "title_model": row.get("title_model", ""),
            "title_truth": row.get("title_truth", ""),
            "title_similarity": round(title_score, 3),
            "title_match": "✅" if title_ok else "❌",

            "document_type_model": row.get("document_type_model", ""),
            "document_type_truth": row.get("document_type_truth", ""),
            "document_type_match": "✅" if doc_type_match else "❌",

            "summary_model": row.get("summary_model", ""),
            "summary_truth": row.get("summary_truth", ""),
            "summary_similarity": round(summary_score, 3),
            "summary_match": "✅" if summary_ok else "❌",

            "row_score_percent": round(row_score, 2),
        })

    result_df = pd.DataFrame(results)
    report_path = os.path.join(
        OUTPUT_FOLDER, os.path.basename(model_path).replace(".csv", "_validation_report.csv")
    )
    result_df.to_csv(report_path, index=False)
    print(f"📄 Validation report saved: {report_path}")

    # Overall score (all 5 fields)
    score_cols = ["author_match", "date_match", "title_match", "summary_match", "document_type_match"]
    matches = (result_df[score_cols] == "✅").sum().sum()
    possible = len(result_df) * len(score_cols)
    score = (matches / possible) * 100 if possible > 0 else 0
    return score

# --- Main ---
if __name__ == "__main__":
    ground_encoding = detect_encoding(GROUND_TRUTH_PATH)
    ground_df = pd.read_csv(GROUND_TRUTH_PATH, encoding=ground_encoding)

    model_files = [
        os.path.join(MODEL_RESULTS_FOLDER, f)
        for f in os.listdir(MODEL_RESULTS_FOLDER)
        if f.endswith(".csv")
    ]

    scores = {}
    for model_file in model_files:
        score = validate_model(model_file, ground_df.copy())  # pass copy so we don’t mutate ground_df
        scores[os.path.basename(model_file)] = score

    print("\n📊 Model Evaluation Results:")
    for model, score in scores.items():
        print(f"{model}: {score:.2f}% match against ground truth")

    best_model = max(scores, key=scores.get)
    print(f"\n🏆 Best Model: {best_model} with {scores[best_model]:.2f}% match")
