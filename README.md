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
    - Select the component and tools for our application.
    - Design the flow of data.
    - comunicate with client about the design.
    - Research and build sample code.
  - Model selection and testing( model.py, metadata_output folder)
    - Design data processing.
    - Testing the model.
    - Build the tools for integrate our data processing to our application. 
  - Checking all the process to make sure it work as design.
  - Provide the examples for each process.


Kenrick Lim
- Building MongoDB environment(app.py)
  - Implemented the database connection and data flow logic between Flask and MongoDB using PyMongo.
  - Configured local collections and created 3 logical folders(image_link,json_result,progress)to manage image batches and LLM-generated JSON metadata.
- Assisting in Processing Page(ProcessingPage.html)
  - Create as status whetere the file has been processed out of N files.
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
- Cross-validated the JSON metadata capture process and ensured that the data was captured in MongoDB.

Yasveer Singh
-Develop a processing page(ProcessignPage.html)
-Added in a additional web feature that shows up when process is hit

Setup Instructions:
## 1. DOCKER 
build docker image from docker file

## 2. Open in Browser

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


