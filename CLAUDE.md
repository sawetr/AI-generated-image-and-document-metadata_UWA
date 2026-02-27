# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask web application for extracting structured metadata from document images using Vision-Language Models (VLLMs). Users upload images/documents, the app processes them in batches using Llama.cpp with VLLM models, and results are stored in MongoDB with a web interface for viewing/downloading.

## Running the Application

```bash
# Ensure MongoDB is running locally on port 27017
# Set up environment variables in .env (see .env.example)
python app.py
```

Access at http://127.0.0.1:5000

For Docker deployment, build from the Dockerfile and run the container.

## Architecture

### Core Application (`app.py`)

Flask app with MongoDB integration using PyMongo. Key architectural components:

- **Model Loading**: Llama.cpp with Llava15ChatHandler for vision capabilities. Model paths configured in `.env`
- **Async Processing**: Uses threading (`BATCH_SIZE=10`) to process images without blocking the web interface
- **Progress Tracking**: MongoDB `progress` collection stores real-time processing status (total/completed counts)
- **Job Management**: Each upload gets a UUID `job_id` for tracking

### MongoDB Structure

- Database: `llm_app`
- Collections:
  - `json_results`: Stores completed metadata results per job
  - `image_link`: Maps uploaded images to job_id
  - `progress`: Tracks processing status (total/completed)

### Model Integration

Uses `llama-cpp-python` with vision support via `Llava15ChatHandler`. Compatible models:
- Gemma-3-12B-it-GGUF
- Gemma-3-27B-it-QAT-GGUF
- Qwen2.5-VL-7B-Instruct-GGUF

Model files expected at paths defined in `.env`:
```
MODEL_PATH = "model/gemma-3-27B-it-QAT-Q4_0.gguf"
MMPROJ_PATH = "model/mmproj-model-f16.gguf"
```

The `generate_metadata()` function converts images to base64 data URIs and extracts structured JSON metadata with fields: `author`, `date`, `Title`, `summary`, `document_type`.

### Data Flow

1. User uploads files → `POST /upload` saves with UUID filenames to `uploads/<job_id>/`
2. Background thread `process_job()` processes images in batches
3. Progress updated in MongoDB as each image completes
4. Frontend polls `GET /api/jobs/<job_id>/progress` for status
5. On completion, redirect to results page for JSON/CSV download

### Supporting Scripts

- **`model.py`**: Standalone batch processing script for images in a directory. Externally callable `generate_metadata(image_path)` function returns JSON metadata.
- **`validation.py`**: Validation pipeline comparing model outputs against ground truth. Uses:
  - SentenceTransformer (`all-MiniLM-L6-v2`) for semantic similarity on title/summary
  - Rapidfuzz for fuzzy matching on author/document_type
  - Flexible date normalization and document type matching
  - Reports saved to `Validation_Reports/`
- **`group_*.py`**: Convert JSON metadata outputs to CSV format

### Frontend Structure

Templates use Bootstrap. Key pages:
- `index.html`: File upload interface
- `ProcessingPage.html`: Shows progress bar with polling to progress API
- `results.html`: Displays results table with JSON/CSV download buttons

## Environment Configuration

The `.env` file contains:
- `MODEL_PATH`: Path to main GGUF model file
- `MMPROJ_PATH`: Path to vision projector model
- `mongo_uri`: MongoDB connection string

## Output Directories

- `uploads/`: Temporary storage for uploaded images (organized by job_id)
- `results/`: Generated CSV/JSON results (legacy, app now uses MongoDB)
- `metadata_output_*/`: Batch processing outputs from `model.py`
- `Validation_Reports/`: Validation report CSVs from `validation.py`
