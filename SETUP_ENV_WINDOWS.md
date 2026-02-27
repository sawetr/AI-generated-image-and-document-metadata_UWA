# Setting Up Your .env File (Windows)

## Quick Steps

1. **Copy the template file**
   - Find `.env.sample.windows` in the project folder
   - Right-click and select "Copy"
   - Paste in the same folder
   - Rename the copy to `.env`

2. **Verify the paths** (usually no changes needed if model folder is in project directory)

3. **Save and close** the file

4. **Start the application** by double-clicking `START_WINDOWS.bat`

---

## What Does This File Do?

The `.env` file tells the application where to find:
- The AI model files
- Your MongoDB database

---

## Do I Need to Edit It?

**Most likely NO** - if you followed the setup guide and put the model files in the `model/` folder.

Only edit if:
- Your model files are in a different location
- Your MongoDB is on a different computer or port

---

## How to Edit (If Needed)

1. Right-click `.env` → "Open with" → "Notepad"
2. Change the paths as needed
3. File → Save
4. Close and restart the application

---

## Example: Changing to Absolute Paths

If your model files are in a different location, update the paths like this:

```env
MODEL_PATH = C:\Users\YourName\Downloads\model\gemma-3-27B-it-QAT-Q4_0.gguf
MMPROJ_PATH = C:\Users\YourName\Downloads\model\mmproj-model-f16.gguf
```

**Important:**
- Use forward slashes `/` or double backslashes `\\`
- Make sure file names match exactly

---

## Troubleshooting

### Problem: "Model file not found"
**Solution:** Check that the paths in `.env` point to the actual location of your model files.

### Problem: "MongoDB connection failed"
**Solution:** Make sure MongoDB Desktop is running. The default URI usually works: `mongodb://localhost:27017/`

### Problem: Application won't start after editing .env
**Solution:** Check for typos in the file names and paths. File names are case-sensitive.

---

## Security Note

Never commit the actual `.env` file to Git if it contains sensitive information (passwords, API keys, etc.). The `.env.sample.windows` file is safe to share.
