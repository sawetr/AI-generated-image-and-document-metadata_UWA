from pymongo import MongoClient
import gridfs
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import io

# --- Connection ---
client = MongoClient('mongodb://localhost:27017/')
db = client['image_database']

# --- Create a GridFS object ---
# This object will interact with the fs.files and fs.chunks collections
fs = gridfs.GridFS(db)

def display_image_from_database(filename):
    """
    Retrieve and display an image from MongoDB GridFS
    
    Args:
        filename (str): The filename of the image to retrieve and display
    
    Returns:
        bool: True if image was found and displayed, False otherwise
    """
    try:
        # Find the image by filename
        grid_out = fs.find_one({'filename': filename})
        
        if grid_out:
            # Read the image data
            image_data = grid_out.read()
            
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Display using matplotlib
            plt.figure(figsize=(10, 8))
            plt.imshow(image)
            plt.axis('off')  # Hide axes
            plt.title(f"Retrieved Image: {filename}")
            plt.tight_layout()
            plt.show()
            
            print(f"✅ Successfully displayed '{filename}' from database")
            return True
        else:
            print(f"❌ Image '{filename}' not found in database")
            return False
            
    except Exception as e:
        print(f"❌ Error displaying image '{filename}': {e}")
        return False

def list_images_in_database():
    """
    List all images stored in the GridFS database
    
    Returns:
        list: List of filenames stored in the database
    """
    try:
        # Get all files from GridFS
        files = fs.find()
        filenames = []
        
        print("📁 Images in database:")
        for file in files:
            filename = file.filename
            file_size = file.length
            upload_date = file.upload_date
            filenames.append(filename)
            print(f"  - {filename} (Size: {file_size} bytes, Uploaded: {upload_date})")
        
        return filenames
        
    except Exception as e:
        print(f"❌ Error listing images: {e}")
        return []

# --- Store the image using GridFS ---
image_path = '/Users/sawetr/Documents/UWA_project/AI-generated-image-and-document-metadata_UWA/image/20250801_120107.jpg'
image_name = os.path.basename(image_path)

try:
    with open(image_path, 'rb') as image_file:
        # The put method stores the file and returns its _id
        file_id = fs.put(image_file, filename=image_name, content_type='image/jpeg')
        print(f"🖼️  Successfully stored '{image_name}' using GridFS. File ID: {file_id}")

except FileNotFoundError:
    print(f"❌ Error: The file '{image_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")


# --- Retrieve the image from GridFS ---
# You can find files by filename or any other metadata you stored
grid_out = fs.find_one({'filename': image_name})

if grid_out:
    # The 'grid_out' object is a file-like object, you can read from it
    output_data = grid_out.read()
    
    # Write the data to a new file
    with open('retrieved_from_gridfs.jpg', 'wb') as output_file:
        output_file.write(output_data)
    print("✅ Successfully retrieved the image from GridFS and saved it.")
    
    # Display the retrieved image
    display_image_from_database(image_name)
    
else:
    print(f"Could not find '{image_name}' in GridFS.")

# --- List all images in database ---
print("\n" + "="*50)
available_images = list_images_in_database()

# --- Demo: Display a specific image ---
if available_images:
    print(f"\n🖼️  Displaying the first available image...")
    display_image_from_database(available_images[0])

client.close()