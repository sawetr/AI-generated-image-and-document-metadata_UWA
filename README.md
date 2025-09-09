# AI-Generated Image and Document Metadata Extractor (UWA Project)

This project provides a **Flask-based web interface** that allows users to upload images/documents.  
Uploaded files are processed by an **AI model** (using `llama-cpp-python`) to extract structured metadata (author, date, summary, document type).  
Results are displayed in the browser and can be downloaded in **CSV** and **JSON** formats.  

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd AI-generated-image-and-document-metadata_UWA

## 2. Create a Virtual Environment

It’s recommended to use a virtual environment so dependencies don’t interfere with your system Python.

# Create venv
python3 -m venv venv

# Activate venv (Mac/Linux)
source venv/bin/activate

# Activate venv (Windows PowerShell)
venv\Scripts\activate


Once activated, your terminal prompt will show (venv).

## 3. Install Requirements

Make sure you have pip updated, then install dependencies from requirements.txt.

pip install --upgrade pip
pip install -r requirements.txt


If you run into issues with llama-cpp-python on macOS, you may need:

brew install cmake gcc

## 4. Run the App

Start the Flask server:

python3 app.py


You should see output like:

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000


Open your browser at:
👉 http://127.0.0.1:5000

## 5. Usage

Go to the home page.

Upload one or more image/document files.

Click Process.

View results in the browser.

Download results as CSV or JSON.

📂 Project Structure
AI-generated-image-and-document-metadata_UWA/
│── app.py              # Flask web application
│── model.py            # AI model integration (llama-cpp)
│── requirements.txt    # Project dependencies
│── README.md           # Setup & usage guide
│── uploads/            # Uploaded files (ignored by Git)
│── results/            # Generated CSV/JSON results (ignored by Git)
│── templates/          # HTML templates (index.html, results.html)
│── static/             # CSS/JS styling files
│── .gitignore          # Prevents committing venv, cache, uploads, etc.

👥 Notes for Developers

If model.py is not working (missing llama-cpp), you can temporarily use dummy metadata inside app.py to keep the app running.

Always activate the virtual environment before running the app.

Don’t commit venv/, uploads/, or results/ — they are already excluded via .gitignore.