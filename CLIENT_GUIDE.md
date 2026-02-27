# Quick Start Guide - AI Image & Document Metadata

**For Non-Technical Users - 3 Simple Steps to Get Started**

---

## What is this application?

This application uses AI to automatically extract information from your images and documents, including:
- Author name
- Document title
- Date
- Summary description
- Document type

---

## Prerequisites (One-time setup)

### Step 1: Install Docker Desktop

Docker is a free tool that runs the application in a safe, isolated environment.

**Download Docker Desktop:**
- Windows: https://www.docker.com/products/docker-desktop
- Mac: https://www.docker.com/products/docker-desktop

**Install and run Docker Desktop:**
1. Download and run the installer
2. After installation, open Docker Desktop from your applications/start menu
3. Wait for the Docker icon to appear in your taskbar/menu bar
4. The Docker icon should show "Docker Desktop is running" or similar status

> **Important:** Docker Desktop must be running (not just installed) before you start the application.

---

## Starting the Application

### Windows Users

1. Double-click `START_WINDOWS.bat`
2. Wait for the "READY!" message
3. Open your browser and go to: **http://127.0.0.1:5000**

### Mac/Linux Users

1. Open a terminal
2. Navigate to this folder
3. Type: `./start.sh` and press Enter
4. Wait for the "READY!" message
5. Open your browser and go to: **http://127.0.0.1:5000**

> **First run only:** The application will download and set up everything automatically. This may take 5-10 minutes. Future starts will be much faster.

---

## Using the Application

### 1. Upload Your Files

- Click "Choose Files" or drag and drop your images
- Supported formats: PNG, JPG, JPEG, WEBP
- You can upload multiple files at once

### 2. Wait for Processing

- A progress bar shows how many files have been processed
- Each file is analyzed by the AI model
- Processing time depends on your computer speed

### 3. View & Download Results

Once processing is complete, you can:

- **View online:** See all extracted information in a table
- **Download CSV:** Save results to open in Excel
- **Download JSON:** Save raw data format

---

## Stopping the Application

### Windows Users
- Double-click `STOP_WINDOWS.bat`

### Mac/Linux Users
- Type: `./stop.sh`

> Note: When you restart your computer, you'll need to start Docker Desktop and run the start script again.

---

## Troubleshooting

### "Docker is not installed or not running"
- Make sure Docker Desktop is installed
- Open Docker Desktop and wait for it to start
- The Docker icon should show it's running

### "Connection refused" or page won't load
- Make sure Docker Desktop is running
- Try running the start script again
- Wait 30 seconds and refresh the page

### Application seems slow
- First run is always slower (downloading components)
- AI processing takes time depending on your computer speed
- This is normal - be patient!

### Files aren't processing
- Check that the image format is supported (PNG, JPG, JPEG, WEBP)
- Try uploading fewer files at once
- Refresh the page and try again

---

## Where are my files?

All files stay on your computer:
- **Uploaded images:** Saved in the `uploads` folder
- **Results:** Saved in the `results` folder
- **Database data:** Stored by Docker (can be kept even after stopping)

---

## Need Help?

If you encounter problems not covered here:

1. Make sure Docker Desktop is running
2. Try restarting the application (stop, then start again)
3. Check for error messages in the terminal/command prompt

---

## System Requirements

- **Windows 10/11, macOS, or Linux**
- **At least 8GB RAM** (16GB+ recommended)
- **10GB free disk space**
- **Internet connection** for initial setup

---

*Last updated: February 2026*
