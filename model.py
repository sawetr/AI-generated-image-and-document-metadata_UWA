from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler
import base64
import os
import glob
import json

# --- Configuration ---
# Path to the main GGUF model file
#gemma-3-12b-it-Q4_K_M.gguf
<<<<<<< HEAD
MODEL_PATH = "/Users/sawetr/.lmstudio/models/lmstudio-community/gemma-3-12b-it-GGUF/gemma-3-12b-it-Q4_K_M.gguf"
MMPROJ_PATH = "/Users/sawetr/.lmstudio/models/lmstudio-community/gemma-3-12b-it-GGUF/mmproj-model-f16.gguf"

# Qwen2.5-VL-7B-Instruct-GGUF
# MODEL_PATH = "/Users/sawetr/.lmstudio/models/lmstudio-community/Qwen2.5-VL-7B-Instruct-GGUF/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf"
# MMPROJ_PATH = "/Users/sawetr/.lmstudio/models/lmstudio-community/Qwen2.5-VL-7B-Instruct-GGUF/mmproj-model-f16.gguf"

# gemma-3-27b-it-GGUF
# MODEL_PATH = "/Users/sawetr/.lmstudio/models/lmstudio-community/gemma-3-27B-it-qat-GGUF/gemma-3-27B-it-QAT-Q4_0.gguf"
# MMPROJ_PATH = "/Users/sawetr/.lmstudio/models/lmstudio-community/gemma-3-27B-it-qat-GGUF/mmproj-model-f16.gguf"

# Directories for input and output
INPUT_DIRECTORY = "/Users/sawetr/Documents/UWA_project/AI-generated-image-and-document-metadata_UWA/image"
OUTPUT_DIRECTORY = "/Users/sawetr/Documents/UWA_project/AI-generated-image-and-document-metadata_UWA/metadata_output_gemma3-12b"
=======
# MODEL_PATH = r"C:\Users\17740\.lmstudio\models\lmstudio-community\gemma-3-12b-it-GGUF\gemma-3-12b-it-Q3_K_L.gguf"
# MMPROJ_PATH = r"C:\Users\17740\.lmstudio\models\lmstudio-community\gemma-3-12b-it-GGUF\mmproj-model-f16.gguf"

# Qwen2.5-VL-7B-Instruct-GGUF (Recommended - More Stable)
MODEL_PATH = "/Users/sawetr/.lmstudio/models/lmstudio-community/Qwen2.5-VL-7B-Instruct-GGUF/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf"
MMPROJ_PATH = "/Users/sawetr/.lmstudio/models/lmstudio-community/Qwen2.5-VL-7B-Instruct-GGUF/mmproj-model-f16.gguf"

# gemma-3-27b-it-GGUF (Larger model - may have stability issues)
# MODEL_PATH = "/Users/sawetr/.lmstudio/models/lmstudio-community/gemma-3-27B-it-qat-GGUF/gemma-3-27B-it-QAT-Q4_0.gguf"
# MMPROJ_PATH = "/Users/sawetr/.lmstudio/models/lmstudio-community/gemma-3-27B-it-qat-GGUF/mmproj-model-f16.gguf"

# Directories for input and output
INPUT_DIRECTORY = "/Users/sawetr/Documents/UWA_project/AI-generated-image-and-document-metadata_UWA/image"
OUTPUT_DIRECTORY = "/Users/sawetr/Documents/UWA_project/AI-generated-image-and-document-metadata_UWA/metadata_output_qwen25"

# Detect model type and set appropriate parameters
MODEL_TYPE = "qwen" if "Qwen" in MODEL_PATH else "gemma"
if MODEL_TYPE == "gemma":
    CTX_SIZE = 4096
    MAX_TOKENS = 512
    N_BATCH = 256
else:  # qwen
    CTX_SIZE = 2048  
    MAX_TOKENS = 1024
    N_BATCH = 512
>>>>>>> yujie

# --- Load the model once ---
print("🧠 Loading VLLM model... (The first call is slightly slower.)")
chat_handler = Llava15ChatHandler(clip_model_path=MMPROJ_PATH, verbose=False)
llm = Llama(
    model_path=MODEL_PATH,
    chat_handler=chat_handler,
    n_ctx=CTX_SIZE,          # Dynamic context size based on model
    n_gpu_layers=-1,
    n_batch=N_BATCH,         # Dynamic batch size
    n_threads=4,             # Limit CPU threads for stability
    verbose=False
)

# --- Helper Function to Encode Image ---
def image_to_base64_data_uri(file_path):
    """Reads an image file and converts it to a base64 data URI."""
    with open(file_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded_string}"

# --- New Interface: Externally Callable ---
def generate_metadata(image_path):
    """
    External API call: Input image_path, return JSON dictionary
    """
<<<<<<< HEAD
    image_uri = image_to_base64_data_uri(image_path)
    system_prompt = """
    You are an expert document analyst AI. Your task is to extract structured metadata from the document image provided.
    The metadata must be in a valid JSON format and include: "author", "date" (in YYYY-MM-DD format), "Title" you can create one if you can't find any, a one-sentence "summary", and the "document_type".
    If a value cannot be found, use "Unknown",except "Title" that can be created.
    Output ONLY the raw JSON object, without any other text or markdown.
    """
    user_prompt = "Please analyze this document image and extract its metadata."
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image_uri}},
                {"type": "text", "text": user_prompt},
            ],
        },
    ]
=======
    try:
        image_uri = image_to_base64_data_uri(image_path)
        system_prompt = """
        You are an expert document analyst AI. Your task is to extract structured metadata from the document image provided.
        The metadata must be in a valid JSON format and include: "author", "date" (in YYYY-MM-DD format), a one-sentence "summary", and the "document_type".
        If a value cannot be found, use "Unknown".
        Output ONLY the raw JSON object, without any other text or markdown.
        """
        user_prompt = "Please analyze this document image and extract its metadata."
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_uri}},
                    {"type": "text", "text": user_prompt},
                ],
            },
        ]
>>>>>>> yujie

        # The response is enforced to be JSON only
        response = llm.create_chat_completion(
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=512,  # Limit tokens for Gemma-27B
            stream=False     # Ensure non-streaming response
        )
        
        if not response or 'choices' not in response or not response['choices']:
            raise ValueError("Invalid response from model")
            
        raw_json = response['choices'][0]['message']['content']
        if not raw_json:
            raise ValueError("Empty response from model")
            
        metadata = json.loads(raw_json)
        return metadata
        
    except Exception as e:
        print(f"❌ Error in generate_metadata: {e}")
        return {
            "error": f"Model processing failed: {str(e)}",
            "author": "Unknown",
            "date": "Unknown", 
            "summary": "Failed to process image",
            "document_type": "Unknown"
        }


# --- Main Execution ---
def main():
    """
    Main function to orchestrate the batch processing of images using a VLLM.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    # --- Load the VLLM (LLM + Vision Projector) once ---
    print("🧠 Loading VLLM model... (This may take a moment)")

    # Find all supported image files in the input directory
    image_paths = glob.glob(os.path.join(INPUT_DIRECTORY, '*.[pP][nN][gG]')) + \
                  glob.glob(os.path.join(INPUT_DIRECTORY, '*.[jJ][pP][gG]')) + \
                  glob.glob(os.path.join(INPUT_DIRECTORY, '*.[jJ][pP][eE][gG]')) + \
                  glob.glob(os.path.join(INPUT_DIRECTORY, '*.[wW][eE][bB][pP]'))

    if not image_paths:
        print(f"❌ No images found in '{INPUT_DIRECTORY}'. Please add images to process.")
        return

    print(f"\nFound {len(image_paths)} images. Starting VLLM batch processing...\n")

    # --- Loop through each image and process it directly ---
    for image_path in image_paths:
        image_filename = os.path.basename(image_path)
        print(f"--- Processing: {image_filename} ---")

        # 1. Convert image to data URI for the model
        image_uri = image_to_base64_data_uri(image_path)
        
        # 2. Create the prompt for the VLLM
        system_prompt = """
        You are an expert document analyst AI. Your task is to extract structured metadata from the document image provided.
        The metadata must be in a valid JSON format and include: "author","date" (in YYYY-MM-DD format),"Title" you can create one if you can't find any, a one-sentence "summary", and the "document_type".
        If a value cannot be found, use "Unknown",except "Title" that can be created.
        Output ONLY the raw JSON object, without any other text or markdown.
        """
        
        user_prompt = "Please analyze this document image and extract its metadata."

        # The message format for VLLMs includes the image data directly
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_uri}},
                    {"type": "text", "text": user_prompt},
                ],
            },
        ]

        # 3. Generate metadata
        print("🤖 Generating metadata from image...")
        try:
            response = llm.create_chat_completion(
                messages=messages,
                response_format={"type": "json_object"}, # Enforce JSON output
                temperature=0.1
            )
            json_output = response['choices'][0]['message']['content']
            metadata = json.loads(json_output)
            
            # 4. Save the metadata to a JSON file
            base_name = os.path.splitext(image_filename)[0]
            output_filename = f"{base_name}_metadata.json"
            output_path = os.path.join(OUTPUT_DIRECTORY, output_filename)

            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=4)
            
            print(f"✅ Metadata saved to '{output_path}'\n")

        except (json.JSONDecodeError, KeyError) as e:
            print(f"❌ Failed to parse JSON for {image_filename}. Error: {e}")
            if 'response' in locals():
                print("Raw response:", response['choices'][0]['message']['content'])
            print("")
        except Exception as e:
            print(f"❌ An unexpected error occurred while processing {image_filename}: {e}\n")


if __name__ == "__main__":
    main()