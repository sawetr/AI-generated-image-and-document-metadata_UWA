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
  - Planning evaluation methods and checking the model. 
  - Checking all the process to make sure it work as design.
  - Provide the examples for each process.

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
- Developed and conducted human evaluation scoring methodology to serve as cross-validation of the programmed evaluation scores.
- Created the Dockerfile and requirements package necessary to run a Docker-based implementation.
- Created the comprehensive installation guide to install and run the Docker-based implementation.
- Assisted in setting up MongoDB integrations (e.g. MongoDB Compass) through initial mocks of JSON metadata output through Streamlit.
- Cross-validated the JSON metadata capture process and ensured that the data was captured in MongoDB.


Yasveer Singh

-Develop a processing page(ProcessignPage.html)
-Added in a additional web feature that shows up when process is hit

Click on this for the [comprehensive installation guide](https://github.com/sawetr/AI-generated-image-and-document-metadata_UWA/blob/Installation-Branch/installation.md) 

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


