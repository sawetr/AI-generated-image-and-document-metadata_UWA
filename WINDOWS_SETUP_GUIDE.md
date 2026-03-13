# Complete Windows Setup Guide
## AI Image & Document Metadata Application

---

## Table of Contents
1. [Before You Start](#before-you-start)
2. [Step 1: Install Docker Desktop](#step-1-install-docker-desktop)
3. [Step 2: Prepare the Model Files](#step-2-prepare-the-model-files)
4. [Step 3: Start the Application](#step-3-start-the-application)
5. [Step 4: Using the Application](#step-4-using-the-application)
6. [Step 5: Stopping the Application](#step-5-stopping-the-application)
7. [Troubleshooting](#troubleshooting)
8. [Frequently Asked Questions](#frequently-asked-questions)

---

## Before You Start

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Operating System | Windows 10 (64-bit) | Windows 11 |
| RAM | 8GB | 16GB or more |
| Free Disk Space | 20GB | 30GB or more |
| Internet | Required for setup | Required for setup |

### What You'll Get After Setup

- A web application running on your computer at `http://127.0.0.1:5000`
- AI-powered document metadata extraction
- Results saved to your computer
- All data stays local (privacy-friendly)

## Install VS code
Download from vs code website.
## install GIT (Version control)
Download from git website. 
---

## Step 1: Install Docker Desktop

### Why Do You Need Docker?

Docker is a tool that runs the application in a safe, isolated "container" - like a virtual computer within your computer. It handles all the complex technical stuff automatically.

### Installation Steps

#### 1.1 Download Docker Desktop

1. Go to: **https://www.docker.com/products/docker-desktop**
2. Click "Download for Windows"
3. Wait for the download to complete (~500MB)

#### 1.2 Install Docker Desktop

1. Find the downloaded file (usually in your Downloads folder)
2. Double-click `Docker Desktop Installer.exe`
3. Follow the installation wizard:
   - Click "OK" or "Yes" for all prompts
   - Leave all settings as default (recommended)
   - Check "Use WSL 2 instead of Hyper-V" if prompted (recommended)
4. Click "Close" when installation is complete

#### 1.3 Start Docker Desktop

1. Open Docker Desktop from:
   - Start Menu → "Docker Desktop"
   - Or double-click the Docker icon on your desktop

2. **Important:** Wait for Docker to fully start!
   - Look for the Docker icon in your taskbar (bottom-right corner, near the clock)
   - The icon should stop spinning and show a solid image
   - Hover over the icon - it should say "Docker Desktop is running"

3. Accept the Docker Service Terms if prompted
4. Docker will now download additional components - this may take a few minutes

#### 1.4 Verify Docker is Running

1. Open Command Prompt:
   - Press `Windows Key`, type `cmd`, press Enter

2. Type the following command and press Enter:
   ```
   docker --version
   ```

3. You should see output like:
   ```
   Docker version 24.x.x
   ```

If you see this, Docker is installed and running! 🎉

> **Troubleshooting:** If you get an error, make sure Docker Desktop is open and the icon shows "running".

---

## Step 2: Prepare the Model Files

### What Are the Model Files?

The AI model is what analyzes your documents. It's a large file (about 15GB) that contains the "brain" of the AI.

### Option A: Model Files Are Already Included

If the project folder already contains the `model/` folder with these files:
- `gemma-3-27B-it-QAT-Q4_0.gguf` (~14GB)
- `mmproj-model-f16.gguf` (~818MB)

You can skip to **Step 3**!

### Option B: You Need to Download the Model Files

If the model folder is empty or missing, follow these steps:

#### 2.1 Locate the Model Folder

1. Open the project folder: `AI-generated-image-and-document-metadata_UWA`
2. Look for a folder named `model`
3. If it doesn't exist, create it:
   - Right-click in the folder → New → Folder
   - Name it: `model`

#### 2.2 Download the Model Files

Contact the development team to get the model files. You should receive:
1. `gemma-3-27B-it-QAT-Q4_0.gguf` (main AI model - ~14GB)
2. `mmproj-model-f16.gguf` (vision projector - ~818MB)

#### 2.3 Extract/Place the Model Files

1. Once downloaded, extract the files if they're in a zip archive
2. Move/extract both files into the `model/` folder

Your folder structure should look like:
```
AI-generated-image-and-document-metadata_UWA/
├── model/
│   ├── gemma-3-27B-it-QAT-Q4_0.gguf
│   └── mmproj-model-f16.gguf
├── app.py
├── START_WINDOWS.bat
└── [other files]
```

> **Tip:** The download may take 30 minutes to several hours depending on your internet speed. Be patient!

---

## Step 3: Start the Application

Now the easy part - just double-click!

### 3.1 Start the Application

1. Make sure Docker Desktop is **running** (check the taskbar icon)
2. Navigate to the project folder
3. **Double-click: `START_WINDOWS.bat`**

You'll see a black window open with progress messages.

### 3.2 Wait for Setup to Complete

The first time you run the application, it will:

1. Stop any existing containers
2. Download and build the Docker image (takes 5-10 minutes)
3. Start MongoDB database
4. Start the application

You'll see messages like:
```
[1/4] Stopping any existing containers...
[2/4] Building the application (this may take a few minutes)...
[3/4] Starting MongoDB and the application...
[4/4] Waiting for services to be ready...
```

### 3.3 Application is Ready!

When you see:
```
============================================
READY!
============================================

Open your browser and go to:
http://127.0.0.1:5000
```

The application is ready to use! 🎉

> **Note:** Leave the black window open while you use the application. Closing it will stop the application.

---

## Step 4: Using the Application

### 4.1 Open Your Web Browser

1. Open your web browser (Chrome, Edge, Firefox, Safari)
2. Type this address in the address bar:
   ```
   http://127.0.0.1:5000
   ```
3. Press Enter

You should see the application's upload page.

### 4.2 Upload Your Documents

1. Click "Choose Files" or drag and drop images
2. Select one or more image files
3. Supported formats:
   - PNG
   - JPG / JPEG
   - WEBP
4. Click the "Upload" button

### 4.3 Wait for Processing

1. You'll see a progress page with a progress bar
2. The application processes images in batches of 10
3. Each image is analyzed by the AI model
4. Time depends on:
   - Number of images
   - Your computer's speed
   - First image takes longer (model loads into memory)

### 4.4 View and Download Results

Once processing is complete:

**View Online:**
- Results displayed in a table format
- Shows: filename, author, title, date, summary, document type

**Download as CSV (for Excel):**
1. Click "Download CSV" button
2. Save the file to your computer
3. Open with Excel, Google Sheets, etc.

**Download as JSON (raw data):**
1. Click "Download JSON" button
2. Save for programming/data use

### 4.5 What Information is Extracted?

For each document, the AI extracts:

| Field | Description | Example |
|-------|-------------|---------|
| Author | Who created the document | "John Smith" |
| Title | Document title or subject | "Annual Report 2025" |
| Date | Date of the document | "2025-03-15" |
| Summary | One-sentence description | "This is a financial report showing quarterly earnings." |
| Document Type | Type of document | "invoice", "report", "letter", "contract" |

---

## Step 5: Stopping the Application

When you're done using the application:

### 5.1 Stop the Application

1. Double-click: `STOP_WINDOWS.bat`

Or:

1. Go to the black window with the running application
2. Press `Ctrl + C` (hold Ctrl, press C)
3. Type `Y` and press Enter if asked to terminate

### 5.2 Optional: Stop Docker Desktop

If you want to completely stop everything:

1. Right-click the Docker icon in your taskbar
2. Click "Quit Docker Desktop"

> **Note:** You don't need to stop Docker Desktop unless you want to save computer resources. Leave it running for faster startups next time.

---

## Troubleshooting

### Problem: "Docker is not installed or not running"

**Cause:** Docker Desktop is not installed or not running.

**Solution:**
1. Check if Docker Desktop is installed:
   - Press Windows Key, type "Docker Desktop"
   - If it appears, click to open it
   - Wait for the icon to show "running"

2. If not installed, go back to **Step 1** and install Docker Desktop

3. Verify Docker is running:
   - Open Command Prompt
   - Type: `docker --version`
   - If you see a version number, Docker is working

---

### Problem: "Connection refused" or page won't load at http://127.0.0.1:5000

**Cause:** Application not running, or still starting up.

**Solution:**
1. Make sure the START_WINDOWS.bat window is still open
2. Wait 30 seconds and refresh the page
3. If that doesn't work:
   - Stop the application (double-click STOP_WINDOWS.bat)
   - Start again (double-click START_WINDOWS.bat)
   - Wait for "READY!" message

---

### Problem: "Model file not found" or "No such file or directory"

**Cause:** Model files are missing or in wrong location.

**Solution:**
1. Check the `model/` folder exists
2. Verify both files are present:
   - `gemma-3-27B-it-QAT-Q4_0.gguf`
   - `mmproj-model-f16.gguf`
3. Make sure file names match exactly (case-sensitive)
4. If files are elsewhere, move them to the `model/` folder

---

### Problem: Application is very slow

**Cause:** First-time setup, or computer hardware limitations.

**Solution:**
1. **First run is always slower** - components are being downloaded and installed
2. Check your RAM usage:
   - Open Task Manager (Ctrl+Shift+Esc)
   - Look at "Memory" usage
   - If near 100%, close other applications
3. This is normal - AI processing requires significant computing power

---

### Problem: Files aren't processing

**Cause:** Unsupported format, error during processing.

**Solution:**
1. Check file format:
   - Only PNG, JPG, JPEG, WEBP are supported
   - Try converting unsupported files with an image converter

2. Try uploading fewer files at once

3. Check the START_WINDOWS.bat window for error messages

4. Refresh the page and try again

---

### Problem: "Port 5000 already in use"

**Cause:** Another application is using port 5000.

**Solution:**
1. Find what's using port 5000:
   - Open Command Prompt
   - Type: `netstat -ano | findstr :5000`
   - Note the PID (last number)

2. Close that application, or change the port:
   - Open `docker-compose.yml` with Notepad
   - Find: `"5000:5000"`
   - Change to: `"5001:5000"`
   - Save and restart the application
   - Access at: http://127.0.0.1:5001

---

### Problem: "Failed to start service: llm_mongodb"

**Cause:** MongoDB failed to start.

**Solution:**
1. Stop and restart:
   - Double-click STOP_WINDOWS.bat
   - Double-click START_WINDOWS.bat

2. Check Docker Desktop has enough resources:
   - Open Docker Desktop
   - Settings → Resources
   - Increase memory to at least 4GB
   - Apply and restart Docker

---

## Frequently Asked Questions

### Q: Do I need to keep the black window open?

**A:** Yes, the START_WINDOWS.bat window must stay open for the application to work. Closing it stops the application.

---

### Q: Can I use this without internet?

**A:** No, you need internet for:
- Initial Docker setup (downloading components)
- Installing Docker Desktop

Once set up, the application works offline (AI processing doesn't require internet).

---

### Q: Is my data sent to external servers?

**A:** No, everything runs locally on your computer. Your documents and extracted data never leave your machine.

---

### Q: How long does processing take?

**A:** It depends on:
- Your computer's speed (RAM, CPU, GPU if available)
- Number and size of images
- First image is slower (model loads into memory)

Typical times (rough estimate):
- First image: 30-60 seconds
- Subsequent images: 10-30 seconds each

---

### Q: Can I run multiple uploads at the same time?

**A:** No, wait for one batch to complete before starting another. The application processes all uploaded files together.

---

### Q: What happens if my computer restarts?

**A:** You'll need to:
1. Start Docker Desktop
2. Double-click START_WINDOWS.bat

Your uploaded files and results are saved and will still be there.

---

### Q: Can I install this on multiple computers?

**A:** Yes! Each computer needs:
- Docker Desktop installed
- The project files
- The model files

---

### Q: How do I update the application?

**A:** Contact the development team for updated files. To update:
1. Stop the application (STOP_WINDOWS.bat)
2. Replace/update the project files
3. Start again (START_WINDOWS.bat)

---

### Q: Can I change the AI model to a smaller/faster one?

**A:** Yes, this requires technical setup. Contact the development team for assistance with model switching.

---

### Q: My results folder is getting large. Can I delete old files?

**A:** Yes! You can safely delete:
- Files in `uploads/` folder
- Files in `results/` folder
- These are just temporary/processed copies

---

## Getting Additional Help

If you're still having problems:

1. **Check error messages:** Look at the black window for specific error information
2. **Restart everything:**
   - Close Docker Desktop
   - Open Docker Desktop
   - Run STOP_WINDOWS.bat
   - Run START_WINDOWS.bat
3. **Contact support:** Provide:
   - The error message you see
   - Your Windows version
   - Your RAM/CPU specs
   - Screenshot if possible

---

## Quick Reference

| Action | How to do it |
|--------|--------------|
| Start application | Double-click `START_WINDOWS.bat` |
| Stop application | Double-click `STOP_WINDOWS.bat` |
| Access in browser | Go to http://127.0.0.1:5000 |
| Check if Docker is running | Taskbar should show Docker icon (solid, not spinning) |
| View logs | In the START_WINDOWS.bat window |

---

## Directory Structure

```
AI-generated-image-and-document-metadata_UWA/
├── model/                    # AI model files (DON'T DELETE)
│   ├── gemma-3-27B-it-QAT-Q4_0.gguf
│   └── mmproj-model-f16.gguf
├── uploads/                  # Uploaded images (can be deleted)
├── results/                  # Generated results (can be deleted)
├── app.py                    # Main application
├── START_WINDOWS.bat         # Quick start script
├── STOP_WINDOWS.bat          # Quick stop script
├── Dockerfile                # Docker configuration
├── docker-compose.yml       # Docker orchestration
├── requirements.txt          # Python dependencies
└── [other files]
```

---

*Last updated: February 2026*
*Version: 1.0*
