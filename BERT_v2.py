import os
import pandas as pd
import chardet
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

# --- Paths ---
GROUND_TRUTH_PATH = "Client_Ground_Truth/metadata_Ground_Truth.csv"
MODEL_RESULTS_FOLDER = "Our_AI_Model_Results"
OUTPUT_FOLDER = "Validation_Reports_BERT"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load BERT model
try:
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bert_model = BertModel.from_pretrained('bert-base-uncased')
    bert_model.eval()  # Set to evaluation mode
    print("✅ BERT model loaded successfully")
except Exception as e:
    print(f"❌ Error loading BERT model: {e}")
    tokenizer = None
    bert_model = None

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

def get_bert_embeddings(texts):
    """Get BERT embeddings with mean pooling"""
    if tokenizer is None or bert_model is None:
        return None
    
    try:
        inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = bert_model(**inputs)
        # Use mean pooling of last hidden states
        embeddings = torch.mean(outputs.last_hidden_state, dim=1)
        return embeddings.numpy()
    except Exception as e:
        print(f"Warning: BERT embedding failed: {e}")
        return None

def bert_semantic_similarity(text1, text2):
    """Calculate semantic similarity using BERT embeddings and cosine similarity"""
    if pd.isna(text1) or pd.isna(text2) or text1 == "" or text2 == "":
        return 0.0, False
    
    if str(text1).lower() == "unknown" and str(text2).lower() == "unknown":
        return 1.0, True
    
    embeddings = get_bert_embeddings([str(text1), str(text2)])
    if embeddings is None or len(embeddings) < 2:
        return 0.0, False
    
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return similarity, similarity >= 0.7

# --- BERT Validation Logic ---
def validate_model_bert(model_path, ground_df):
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
        print(f"📄 BERT processing: {filename}_metadata.json ✅")
        
        # Exact matches
        author_exact = exact_match(row.get("author_model", ""), row.get("author_truth", ""))
        
        date_model_norm = normalize_date(row.get("date_model", ""))
        date_truth_norm = normalize_date(row.get("date_truth", ""))
        date_match = date_model_norm == date_truth_norm
        
        title_exact = exact_match(row.get("title", ""), row.get("title_truth", ""))
        
        doc_type_exact = exact_match(row.get("document_type_model", ""), row.get("document_type_truth", ""))
        
        summary_exact = exact_match(row.get("summary_model", ""), row.get("summary_truth", ""))
        
        # BERT semantic matches
        author_bert, author_bert_match = bert_semantic_similarity(
            row.get("author_model", ""), row.get("author_truth", "")
        )
        
        title_bert, title_bert_match = bert_semantic_similarity(
            row.get("title", ""), row.get("title_truth", "")
        )
        
        doc_type_bert, doc_type_bert_match = bert_semantic_similarity(
            row.get("document_type_model", ""), row.get("document_type_truth", "")
        )
        
        summary_bert, summary_bert_match = bert_semantic_similarity(
            row.get("summary_model", ""), row.get("summary_truth", "")
        )

        results.append({
            "filename": filename,
            # Author
            "author_model": row.get("author_model", ""),
            "author_truth": row.get("author_truth", ""),
            "author_exact_match": "✅" if author_exact else "❌",
            "author_bert_similarity": round(author_bert, 3),
            "author_bert_match": "✅" if author_bert_match else "❌",
            # Date
            "date_model": row.get("date_model", ""),
            "date_truth": row.get("date_truth", ""),
            "date_match": "✅" if date_match else "❌",
            # Title
            "title_model": row.get("title", ""),
            "title_truth": row.get("title_truth", ""),
            "title_exact_match": "✅" if title_exact else "❌",
            "title_bert_similarity": round(title_bert, 3),
            "title_bert_match": "✅" if title_bert_match else "❌",
            # Document Type
            "document_type_model": row.get("document_type_model", ""),
            "document_type_truth": row.get("document_type_truth", ""),
            "doc_type_exact_match": "✅" if doc_type_exact else "❌",
            "doc_type_bert_similarity": round(doc_type_bert, 3),
            "doc_type_bert_match": "✅" if doc_type_bert_match else "❌",
            # Summary
            "summary_exact_match": "✅" if summary_exact else "❌",
            "summary_bert_similarity": round(summary_bert, 3),
            "summary_bert_match": "✅" if summary_bert_match else "❌",
        })

    print(f"✅ BERT processed {len(processed_files)} files from {os.path.basename(model_path)}")
    
    result_df = pd.DataFrame(results)
    report_path = os.path.join(OUTPUT_FOLDER, os.path.basename(model_path).replace(".csv", "_bert_report.csv"))
    result_df.to_csv(report_path, index=False)
    print(f"📄 BERT validation report saved: {report_path}")

    # Calculate scores
    total_rows = len(result_df)
    possible_matches = total_rows * 5
    
    exact_matches = (result_df[["author_exact_match", "title_exact_match", "doc_type_exact_match", "summary_exact_match", "date_match"]] == "✅").sum().sum()
    bert_matches = (result_df[["author_bert_match", "title_bert_match", "doc_type_bert_match", "summary_bert_match", "date_match"]] == "✅").sum().sum()
    
    avg_bert_score = result_df[["author_bert_similarity", "title_bert_similarity", "doc_type_bert_similarity", "summary_bert_similarity"]].mean().mean()
    
    exact_score = (exact_matches / possible_matches) * 100 if possible_matches > 0 else 0
    bert_score = (bert_matches / possible_matches) * 100 if possible_matches > 0 else 0

    return exact_score, bert_score, avg_bert_score

# --- Main for BERT version ---
if __name__ == "__main__":
    # Install required packages:
    # pip install transformers torch scikit-learn pandas chardet
    
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

    print(f"🔍 Found {len(model_files)} model file(s) to validate with BERT")

    exact_scores = {}
    bert_scores = {}
    avg_bert_scores = {}
    
    for model_file in model_files:
        print(f"\n--- Validating with BERT: {os.path.basename(model_file)} ---")
        try:
            exact_score, bert_score, avg_bert_score = validate_model_bert(model_file, ground_df)
            model_name = os.path.basename(model_file)
            exact_scores[model_name] = exact_score
            bert_scores[model_name] = bert_score
            avg_bert_scores[model_name] = avg_bert_score
            print(f"✅ BERT validation completed for {model_name}")
        except Exception as e:
            print(f"❌ Error validating {model_file}: {e}")

    if exact_scores:
        print("\n" + "="*60)
        print("🧠 BERT MODEL EVALUATION RESULTS")
        print("="*60)
        
        for model in exact_scores.keys():
            print(f"\n📋 {model}:")
            print(f"   Exact Similarity Score: {exact_scores[model]:.2f}%")
            print(f"   BERT Similarity Score:  {bert_scores[model]:.2f}%")
            print(f"   Avg BERT Cosine Similarity: {avg_bert_scores[model]:.3f}")

        best_model_exact = max(exact_scores, key=exact_scores.get)
        best_model_bert = max(bert_scores, key=bert_scores.get)
        best_model_cosine = max(avg_bert_scores, key=avg_bert_scores.get)
        
        print(f"\n🏆 Best by Exact Match: {best_model_exact} ({exact_scores[best_model_exact]:.2f}%)")
        print(f"🏆 Best by BERT Match: {best_model_bert} ({bert_scores[best_model_bert]:.2f}%)")
        print(f"🏆 Best by Cosine Similarity: {best_model_cosine} ({avg_bert_scores[best_model_cosine]:.3f})")
        print(f"\n📁 BERT reports saved in: {OUTPUT_FOLDER}")
    else:
        print("❌ No models were successfully validated with BERT.")