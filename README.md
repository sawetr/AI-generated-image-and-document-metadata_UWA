# AI-generated-image-and-document-metadata_UWA

Member:
1. Sawetr Suchit-rattanant
2. Kenrick Lim
3. Arzoo Arzoo
4. Yujie YANG
5. Gideon Tan
6. Yashveer Singh

Contribution 

Sawetr Suchit-rattanant 
  - Design the project
  - Model selection and testing( model.py, metadata_output folder)
  - Evaluation (Human evaluation)
  - Checking the process

Kenrick Lim
- Building MongoDB environment(app.py)
- Assisting in Processing Page(ProcessingPage.html)
  
Arzoo Arzoo
- Added web functionality, developed the entire frontend (HTML and CSS) and built the project webpage(static and results folder)
- Added requirements file and updated README for reproducibility
- Implemented validation pipeline (validate.py) and integrated validation results into CSV reports (Validation_Reports folder)
- Added fuzzy and embedding-based semantic similarity checks for title and summary
- Iteratively tested, debugged, and refined validation workflow against ground truth

Yujie YANG
- Integrate the frontend upload process with the AI model, batching client images for metadata generation and returning the formatted output to the web interface. (app.py).
- Created ground-truth files and contributed to human evaluation for model assessment.

Gideon Tan
- Assisted in setting up MongoDB integrations (e.g. MongoDB Compass) through initial mocks of JSON metadata output through Streamlit.
- Developed evaluation checks using various similarity measures (e.g. Cosine Similarity, BERT, SBERT) to evaluate each model's performance in processing the dataset.
- Cross-validated the JSON metadata capture process and ensured that the data was captured in MongoDB.

Setup Instructions:
## 1. Create a Virtual Environment

Mac/Linux

python3 -m venv venv
source venv/bin/activate


Windows (PowerShell)

python -m venv venv
.\venv\Scripts\activate

## 2. Install Dependencies
pip install flask pandas pillow

## 3. Run the App
python3 app.py

## 4. Open in Browser

Go to:

http://127.0.0.1:5000


Upload files → View JSON + CSV results → Download them.

# Project Structure & File Purpose
AI-generated-image-and-document-metadata_UWA/
│── app.py
│── templates/
│   ├── index.html
│   └── results.html
│── static/
│   └── style.css   (optional if you add custom CSS)
│── uploads/
│── results/
│── README.md

app.py → Main Flask app. Handles file uploads, dummy metadata generation, and routing between pages.

templates/index.html → Upload page (frontend).

templates/results.html → Results page (shows JSON + CSV, download buttons).

static/style.css → Optional extra styling (Bootstrap is already used).

uploads/ → Stores uploaded images/documents.

results/ → Stores generated results.csv and results.json.

README.md → Setup guide (this file).

# AI Model Integration (Future Work)

Right now metadata is dummy placeholders.


