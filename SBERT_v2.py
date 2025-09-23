import os
import pandas as pd
import chardet
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import warnings
warnings.filterwarnings('ignore')

# --- Paths ---
GROUND_TRUTH_PATH = "Client_Ground_Truth/metadata_Ground_Truth.csv"
MODEL_RESULTS_FOLDER = "Our_AI_Model_Results"
OUTPUT_FOLDER = "Validation_Reports"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load models (downloads on first run)
try:
    sbert_model = SentenceTransformer("all-mpnet-base-v2")
    print("✅ SBERT model loaded successfully")
except Exception as e:
    print(f"❌ Error loading SBERT model: {e}")
    sbert_model = None

# --- Helpers ---
def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        raw = f.read(100000)
    result = chardet.detect(raw)
    return result["encoding"]

def normalize_date(date_str):
    if pd.isna(date_str) or str(date_str).lower() == "unknown":
        return "unknown"
    try:
        return pd.to_datetime(str(date_str), errors="coerce").strftime("%Y-%m")
    except:
        return str(date_str).strip().lower()

def normalize_string(s):
    if pd.isna(s) or str(s).lower() == "unknown":
        return ""
    return str(s).lower().strip()

def exact_match(str1, str2):
    return normalize_string(str1) == normalize_string(str2)

def semantic_similarity(text1, text2):
    """Calculate semantic similarity using SBERT embeddings and cosine similarity."""
    if pd.isna(text1) or pd.isna(text2) or text1 == "" or text2 == "":
        return 0.0, False
    
    if str(text1).lower() == "unknown" and str(text2).lower() == "unknown":
        return 1.0, True
    
    if sbert_model is None:
        return 0.0, False
    
    try:
        # Generate embeddings
        embeddings = sbert_model.encode([str(text1), str(text2)])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(
            embeddings[0].reshape(1, -1), 
            embeddings[1].reshape(1, -1)
        )[0][0]
        
        return similarity, similarity >= 0.7
    except Exception as e:
        print(f"Warning: Semantic similarity failed: {e}")
        return 0.0, False

# --- Enhanced Validation Logic ---
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
    processed_files = set()
    
    for _, row in merged.iterrows():
        filename = row["filename"]
        processed_files.add(filename)
        print(f"📄 SBERT processing: {filename}_metadata.json ✅")
        
        # Exact matches
        author_exact = exact_match(row.get("author_model", ""), row.get("author_truth", ""))
        
        date_model_norm = normalize_date(row.get("date_model", ""))
        date_truth_norm = normalize_date(row.get("date_truth", ""))
        date_match = date_model_norm == date_truth_norm
        
        title_exact = exact_match(row.get("title", ""), row.get("title_truth", ""))
        
        doc_type_exact = exact_match(row.get("document_type_model", ""), row.get("document_type_truth", ""))
        
        # Semantic analysis
        author_semantic, author_semantic_match = semantic_similarity(
            row.get("author_model", ""), row.get("author_truth", "")
        )
        
        title_semantic, title_semantic_match = semantic_similarity(
            row.get("title", ""), row.get("title_truth", "")
        )
        
        doc_type_semantic, doc_type_semantic_match = semantic_similarity(
            row.get("document_type_model", ""), row.get("document_type_truth", "")
        )
        
        # Summary analysis
        summary_exact = exact_match(row.get("summary_model", ""), row.get("summary_truth", ""))
        summary_semantic, summary_semantic_match = semantic_similarity(
            row.get("summary_model", ""), row.get("summary_truth", "")
        )

        results.append({
            "filename": filename,
            # Author
            "author_model": row.get("author_model", ""),
            "author_truth": row.get("author_truth", ""),
            "author_exact_match": "✅" if author_exact else "❌",
            "author_cosine_similarity": round(author_semantic, 3),
            "author_semantic_match": "✅" if author_semantic_match else "❌",
            # Date
            "date_model": row.get("date_model", ""),
            "date_truth": row.get("date_truth", ""),
            "date_match": "✅" if date_match else "❌",
            # Title
            "title_model": row.get("title", ""),
            "title_truth": row.get("title_truth", ""),
            "title_exact_match": "✅" if title_exact else "❌",
            "title_cosine_similarity": round(title_semantic, 3),
            "title_semantic_match": "✅" if title_semantic_match else "❌",
            # Document Type
            "document_type_model": row.get("document_type_model", ""),
            "document_type_truth": row.get("document_type_truth", ""),
            "doc_type_exact_match": "✅" if doc_type_exact else "❌",
            "doc_type_cosine_similarity": round(doc_type_semantic, 3),
            "doc_type_semantic_match": "✅" if doc_type_semantic_match else "❌",
            # Summary
            "summary_exact_match": "✅" if summary_exact else "❌",
            "summary_cosine_similarity": round(summary_semantic, 3),
            "summary_semantic_match": "✅" if summary_semantic_match else "❌",
        })

    print(f"✅ SBERT processed {len(processed_files)} files from {os.path.basename(model_path)}")
    
    result_df = pd.DataFrame(results)
    report_path = os.path.join(OUTPUT_FOLDER, os.path.basename(model_path).replace(".csv", "_advanced_report.csv"))
    result_df.to_csv(report_path, index=False)
    print(f"📄 Advanced validation report saved: {report_path}")

    # --- Calculate Scores with Error Handling ---
    total_rows = len(result_df)
    possible_matches = total_rows * 5  # 5 fields
    
    # Count successful matches
    exact_matches = (result_df[["author_exact_match", "title_exact_match", "doc_type_exact_match", "summary_exact_match", "date_match"]] == "✅").sum().sum()
    semantic_matches = (result_df[["author_semantic_match", "title_semantic_match", "doc_type_semantic_match", "summary_semantic_match", "date_match"]] == "✅").sum().sum()
    
    # Calculate average scores with error handling
    try:
        avg_cosine = result_df[["author_cosine_similarity", "title_cosine_similarity", "doc_type_cosine_similarity", "summary_cosine_similarity"]].mean().mean()
    except (KeyError, ValueError):
        avg_cosine = 0.0
        print("⚠️  Could not calculate average cosine similarity")
    
    # Calculate percentages
    exact_score = (exact_matches / possible_matches) * 100 if possible_matches > 0 else 0
    semantic_score = (semantic_matches / possible_matches) * 100 if possible_matches > 0 else 0

    return exact_score, semantic_score, avg_cosine

# --- Main ---
if __name__ == "__main__":
    # Install required packages first:
    # pip install sentence-transformers scikit-learn pandas chardet
    
    # Load ground truth data
    try:
        ground_encoding = detect_encoding(GROUND_TRUTH_PATH)
        ground_df = pd.read_csv(GROUND_TRUTH_PATH, encoding=ground_encoding)
        print(f"✅ Successfully loaded ground truth from: {GROUND_TRUTH_PATH}")
    except Exception as e:
        print(f"❌ Error loading ground truth file: {e}")
        exit(1)

    # Check if model results folder exists
    if not os.path.exists(MODEL_RESULTS_FOLDER):
        print(f"❌ Model results folder not found: {MODEL_RESULTS_FOLDER}")
        exit(1)

    # Get all CSV files in the model results folder
    model_files = [os.path.join(MODEL_RESULTS_FOLDER, f) for f in os.listdir(MODEL_RESULTS_FOLDER) if f.endswith(".csv")]
    
    if not model_files:
        print(f"❌ No CSV files found in: {MODEL_RESULTS_FOLDER}")
        exit(1)

    print(f"🔍 Found {len(model_files)} model file(s) to validate")

    exact_scores = {}
    semantic_scores = {}
    cosine_scores = {}
    
    # Validate each model file
    for model_file in model_files:
        print(f"\n--- Validating {os.path.basename(model_file)} with SBERT ---")
        try:
            scores = validate_model(model_file, ground_df)
            model_name = os.path.basename(model_file)
            
            exact_scores[model_name] = scores[0]
            semantic_scores[model_name] = scores[1]
            cosine_scores[model_name] = scores[2]
            
            print(f"✅ SBERT validation completed for {model_name}")
        except Exception as e:
            print(f"❌ Error validating {model_file}: {e}")

    # Display results
    if exact_scores:
        print("\n" + "="*80)
        print("🤖 ADVANCED MODEL EVALUATION RESULTS (SBERT + Cosine)")
        print("="*80)
        
        for model in exact_scores.keys():
            print(f"\n📋 {model}:")
            print(f"   Exact Similarity Score:     {exact_scores[model]:.2f}%")
            print(f"   Semantic Similarity Score:  {semantic_scores[model]:.2f}%")
            print(f"   Avg Cosine Similarity:      {cosine_scores[model]:.3f}")

        # Find best models by different metrics
        best_model_exact = max(exact_scores, key=exact_scores.get)
        best_model_semantic = max(semantic_scores, key=semantic_scores.get)
        best_model_cosine = max(cosine_scores, key=cosine_scores.get)
        
        print(f"\n🏆 Best by Exact Match:    {best_model_exact} ({exact_scores[best_model_exact]:.2f}%)")
        print(f"🏆 Best by Semantic Match: {best_model_semantic} ({semantic_scores[best_model_semantic]:.2f}%)")
        print(f"🏆 Best by Cosine Similarity: {best_model_cosine} ({cosine_scores[best_model_cosine]:.3f})")
        print(f"\n📁 Advanced reports saved in: {OUTPUT_FOLDER}")
    else:
        print("❌ No models were successfully validated.")