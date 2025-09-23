import os
import pandas as pd
import chardet
from rapidfuzz import fuzz

# --- Paths ---
GROUND_TRUTH_PATH = "metadata_Ground_Truth(in).csv"
MODEL_RESULTS_FOLDER = "Our_AI_Model_Results"
OUTPUT_FOLDER = "Validation_Reports"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

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

# --- Validation Logic ---
def validate_model(model_path, ground_df):
    encoding = detect_encoding(model_path)
    print(f"ℹ️ Detected encoding for {model_path}: {encoding}")
    model_df = pd.read_csv(model_path, encoding=encoding)

    # Unify filename column
    if "_filename" in model_df.columns:
        model_df.rename(columns={"_filename": "filename"}, inplace=True)
        model_df["filename"] = model_df["filename"].str.replace("_metadata.json", "", regex=False)

    # Normalize ground truth filename
    ground_df["filename"] = ground_df["filename"].str.replace(".json", "", regex=False)

    # Merge
    merged = pd.merge(model_df, ground_df, on="filename", suffixes=("_model", "_truth"))

    # Compare fields
    results = []
    for _, row in merged.iterrows():
        author_match = fuzzy_match(row.get("author_model", ""), row.get("author_truth", ""))
        date_match = normalize_date(row.get("date_model", "")) == normalize_date(row.get("date_truth", ""))
        title_match = fuzzy_match(row.get("title", ""), row.get("title_truth", ""))
        doc_type_match = fuzzy_match(row.get("document_type_model", ""), row.get("document_type_truth", ""))
        summary_match = fuzzy_match(row.get("summary_model", ""), row.get("summary_truth", ""), threshold=40)

        results.append({
            "filename": row["filename"],
            "author_model": row.get("author_model", ""),
            "author_truth": row.get("author_truth", ""),
            "author_match": "✅" if author_match else "❌",

            "date_model": row.get("date_model", ""),
            "date_truth": row.get("date_truth", ""),
            "date_match": "✅" if date_match else "❌",

            "title_model": row.get("title", ""),
            "title_truth": row.get("title_truth", ""),
            "title_match": "✅" if title_match else "❌",

            "document_type_model": row.get("document_type_model", ""),
            "document_type_truth": row.get("document_type_truth", ""),
            "document_type_match": "✅" if doc_type_match else "❌",

            "summary_match": "✅" if summary_match else "❌"
        })

    result_df = pd.DataFrame(results)
    report_path = os.path.join(OUTPUT_FOLDER, os.path.basename(model_path).replace(".csv", "_validation_report.csv"))
    result_df.to_csv(report_path, index=False)
    print(f"📄 Validation report saved: {report_path}")

    # Return score
    total = len(result_df)
    matches = (result_df[["author_match", "date_match", "title_match", "document_type_match", "summary_match"]] == "✅").sum().sum()
    possible = total * 5
    score = (matches / possible) * 100
    return score

# --- Main ---
if __name__ == "__main__":
    ground_encoding = detect_encoding(GROUND_TRUTH_PATH)
    ground_df = pd.read_csv(GROUND_TRUTH_PATH, encoding=ground_encoding)

    model_files = [os.path.join(MODEL_RESULTS_FOLDER, f) for f in os.listdir(MODEL_RESULTS_FOLDER) if f.endswith(".csv")]

    scores = {}
    for model_file in model_files:
        score = validate_model(model_file, ground_df)
        scores[os.path.basename(model_file)] = score

    print("\n📊 Model Evaluation Results:")
    for model, score in scores.items():
        print(f"{model}: {score:.2f}% match against ground truth")

    best_model = max(scores, key=scores.get)
    print(f"\n🏆 Best Model: {best_model} with {scores[best_model]:.2f}% match")

 