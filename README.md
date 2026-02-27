# AI Image & Document Metadata Extractor

![Docker](https://img.shields.io/badge/docker-supported-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

A web application that uses **Artificial Intelligence** to automatically extract structured metadata from document images. Upload your documents and get instant information extraction including author, title, date, summary, and document type.

---

## 🚀 Quick Start

### Windows Users (Recommended - Easy Setup)

1. **Install Docker Desktop** (one-time)
   - Download from: https://www.docker.com/products/docker-desktop
   - Follow the installation wizard

2. **Start the Application**
   - Double-click `START_WINDOWS.bat`
   - Wait for "READY!" message

3. **Open Your Browser**
   - Go to: http://127.0.0.1:5000
   - Upload your documents!

That's it! 🎉

> For detailed instructions, see: [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md)

### Mac/Linux Users

1. Install Docker Desktop from https://www.docker.com/products/docker-desktop
2. Run: `./start.sh`
3. Open browser: http://127.0.0.1:5000

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **AI-Powered** | Uses advanced Vision-Language Models for accurate extraction |
| **Batch Processing** | Upload multiple documents at once |
| **Real-Time Progress** | See processing status as it happens |
| **Multiple Output Formats** | Download as JSON or CSV (Excel-compatible) |
| **Local Processing** | All data stays on your computer - privacy-focused |
| **Easy Setup** | One-click start with Docker |

### Extracted Metadata

For each document, the application extracts:

| Field | Description | Example |
|-------|-------------|---------|
| **Author** | Document creator | "John Smith" |
| **Title** | Document title or subject | "Annual Report 2025" |
| **Date** | Document date | "2025-03-15" |
| **Summary** | One-sentence description | "Financial report showing quarterly earnings" |
| **Document Type** | Type classification | "invoice", "report", "letter", etc. |

---

## 📋 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **Operating System** | Windows 10/11, macOS, Linux | Any |
| **RAM** | 8GB | 16GB or more |
| **Disk Space** | 20GB | 30GB or more |
| **Docker** | Docker Desktop | Latest version |

### Supported File Formats

- PNG
- JPG / JPEG
- WEBP

---

## 📁 Project Structure

```
AI-generated-image-and-document-metadata_UWA/
├── app.py                      # Main Flask application
├── model/                      # AI model files (not in repo)
├── templates/                  # HTML templates
│   ├── index.html              # Upload page
│   ├── results.html            # Results display
│   └── ProcessingPage.html     # Progress tracking
├── static/                     # Static assets (CSS, images)
├── uploads/                    # Uploaded images (temporary)
├── results/                    # Generated results
├── Dockerfile                  # Docker container definition
├── docker-compose.yml          # Docker orchestration
├── requirements.txt            # Python dependencies
├── .env.sample.windows         # Environment template (Windows)
├── START_WINDOWS.bat           # Quick start (Windows)
├── STOP_WINDOWS.bat            # Stop application (Windows)
├── start.sh                   # Quick start (Mac/Linux)
├── stop.sh                    # Stop application (Mac/Linux)
├── WINDOWS_SETUP_GUIDE.md      # Detailed Windows setup guide
├── CLIENT_GUIDE.md             # Non-technical user guide
├── QUICK_REFERENCE.txt         # Printable quick reference
├── SETUP_ENV_WINDOWS.md        # Environment configuration guide
├── CLAUDE.md                  # AI assistant guide
├── model.py                   # Standalone model processor
├── validation.py              # Model validation pipeline
└── README.md                  # This file
```

---

## 🛠️ Setup Options

### Option 1: Docker (Recommended) ⭐

**Best for:** Most users, especially non-technical

**Pros:**
- One-click setup
- No Python or MongoDB installation needed
- Consistent across all platforms
- Safe and isolated

**Steps:**
1. Install Docker Desktop
2. Run `START_WINDOWS.bat` (Windows) or `./start.sh` (Mac/Linux)
3. Open browser to http://127.0.0.1:5000

See [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md) for detailed instructions.

---

### Option 2: Manual Setup

**Best for:** Developers, users who want full control

**Requirements:**
- Python 3.8+
- MongoDB running locally
- Python dependencies installed

**Steps:**

1. **Install Python and MongoDB**
   ```bash
   # Install Python 3.8+ from python.org
   # Install MongoDB Community Server
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   # Copy the template for Windows users
   cp .env.sample.windows .env
   # Edit .env with your paths if needed
   ```

4. **Start MongoDB**
   ```bash
   # Start MongoDB (default port 27017)
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Open Browser**
   - Go to: http://127.0.0.1:5000

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md) | Complete Windows setup with troubleshooting |
| [CLIENT_GUIDE.md](CLIENT_GUIDE.md) | Simplified guide for non-technical users |
| [QUICK_REFERENCE.txt](QUICK_REFERENCE.txt) | Printable quick reference card |
| [SETUP_ENV_WINDOWS.md](SETUP_ENV_WINDOWS.md) | Environment configuration guide |
| [CLAUDE.md](CLAUDE.md) | Guide for Claude Code AI assistant |

---

## 🔄 Using the Application

### 1. Upload Documents

- Click "Choose Files" or drag and drop images
- Select multiple files at once
- Supported formats: PNG, JPG, JPEG, WEBP

### 2. Wait for Processing

- Progress bar shows completion status
- Documents processed in batches of 10
- First document takes longer (model loads into memory)

### 3. View & Download Results

**View Online:**
- All extracted metadata in a table
- Easy to scan and review

**Download CSV:**
- Opens in Excel, Google Sheets
- Great for data analysis

**Download JSON:**
- Raw data format
- Good for programmatic use

---

## 🛡️ Privacy & Security

- **100% Local Processing:** No data sent to external servers
- **AI Runs Locally:** Model runs on your computer
- **Your Data Stays Yours:** All documents and results stored locally
- **No Cloud Dependencies:** Works offline after setup

---

## 🤖 AI Model Information

The application uses Vision-Language Models (VLLMs):

- **Gemma-3-27B:** High accuracy, larger model (recommended for best results)
- **Gemma-3-12B:** Balanced performance
- **Qwen2.5-VL-7B:** Faster processing, smaller size

Models are quantized GGUF format for efficient local inference.

---

## 🧪 Development & Testing

### Standalone Model Processor

For testing or batch processing without the web interface:

```bash
python model.py
```

This processes all images in the `image/` folder and outputs to `metadata_output/`.

### Validation Pipeline

To validate model outputs against ground truth:

```bash
python validation.py
```

Uses semantic similarity (SentenceTransformer) and fuzzy matching (RapidFuzz).

---

## 📞 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| Docker not running | Open Docker Desktop, wait for icon to show "running" |
| Page won't load | Wait 30 seconds and refresh, or restart the application |
| Model file not found | Check `.env` paths, ensure model files exist |
| Application is slow | First run is slower (downloads required), be patient |
| Port 5000 in use | Edit `docker-compose.yml` to change port |

For more help, see [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md) troubleshooting section.

---

## 🤝 Project Team

| Member | Contributions |
|--------|---------------|
| **Sawetr Suchit-rattanant** | Project design, model selection and testing, data processing pipeline |
| **Kenrick Lim** | MongoDB environment setup, database integration, progress tracking |
| **Arzoo Arzoo** | Frontend development (HTML/CSS), validation pipeline, reproducibility |
| **Yujie YANG** | Frontend-AI integration, image batching, ground-truth creation |
| **Gideon Tan** | Human evaluation methodology, MongoDB integration, Docker setup |
| **Yashveer Singh** | Processing page development, status indicators |

---

## 📄 License

This project is licensed under the MIT License.

---

## 📞 Support

For questions or issues:

1. Check the documentation files in this repository
2. Review the troubleshooting section
3. Contact the development team with error details

---

*Last updated: February 2026*
