# AI-generated-image-and-document-metadata_UWA

Member:
1. Sawetr Suchit-rattanant
2. Kenrick Lim

Contribution 

Sawetr Suchit-rattanant 
  - Design the project
  - Model selection and testing( model.py, metadata_output folder)
  - Evaluation (Human evaluation)
  - Checking the process



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


