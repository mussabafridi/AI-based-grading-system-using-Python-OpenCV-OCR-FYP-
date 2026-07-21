# from fastapi import FastAPI, File, UploadFile, HTTPException
# import openai
# import base64
# import json
# import os
# import re
# import shutil
# from dotenv import load_dotenv
# import uvicorn
# import fitz  # PyMuPDF
# from io import BytesIO
# from PIL import Image

# # Load environment variables
# load_dotenv()

# # Load OpenAI API key from .env
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# app = FastAPI()

# # Ensure necessary folders exist
# DATA_FOLDERS = {
#     "question": "./Question_data",
#     "answer": "./Answer_data"
# }
# TEMP_PDF_FOLDER = "./pdf_pages"
# for folder in DATA_FOLDERS.values():
#     os.makedirs(folder, exist_ok=True)
# os.makedirs(TEMP_PDF_FOLDER, exist_ok=True)

# def encode_image(image_path):
#     """Encodes an image file to base64."""
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

# def extract_json_from_response(response_content):
#     """Extracts valid JSON content from OpenAI's response using regex."""
#     try:
#         json_match = re.search(r"\{.*\}", response_content, re.DOTALL)
#         if json_match:
#             json_string = json_match.group(0)  # Extract JSON part
#             return json.loads(json_string)  # Convert to dict
#         else:
#             raise ValueError("No valid JSON found in response.")
#     except json.JSONDecodeError:
#         raise HTTPException(status_code=500, detail="Invalid JSON structure received from OpenAI.")

# def process_response(response):
#     """Processes the OpenAI API response and extracts JSON data."""
#     response_content = response.choices[0].message.content.strip()
#     return extract_json_from_response(response_content)

# def convert_pdf_to_images(pdf_bytes, pdf_filename):
#     """Converts a PDF file into JPEG images using PyMuPDF (fitz) and saves them in TEMP_PDF_FOLDER."""
#     pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
#     saved_images = []

#     for i in range(len(pdf_document)):  # Iterate through each page
#         page = pdf_document[i]
#         pix = page.get_pixmap()
#         img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#         img_filename = f"{pdf_filename}_page_{i+1}.jpeg"
#         img_path = os.path.join(TEMP_PDF_FOLDER, img_filename)
#         img.save(img_path, format="JPEG")
#         saved_images.append({"page": i + 1, "image_path": img_path})

#     return saved_images

# @app.post("/extract-json/{data_type}")
# async def extract_json(data_type: str, file: UploadFile = File(...)):
#     """Endpoint to upload an image or PDF and extract JSON using OpenAI.
#     - `data_type`: "question" or "answer" (Determines where data is saved)
#     """
#     if data_type not in DATA_FOLDERS:
#         raise HTTPException(status_code=400, detail="Invalid data type. Use 'question' or 'answer'.")

#     try:
#         # Read file bytes
#         file_bytes = await file.read()
#         pdf_filename = os.path.splitext(file.filename)[0]

#         extracted_data = []  # Store extracted JSON data from all pages

#         if file.filename.endswith(".pdf"):
#             # Convert PDF to images and save them
#             images = convert_pdf_to_images(file_bytes, pdf_filename)
#         else:
#             # Handle direct image upload
#             image_path = os.path.join(TEMP_PDF_FOLDER, f"{pdf_filename}.jpeg")
#             with open(image_path, "wb") as f:
#                 f.write(file_bytes)
#             images = [{"page": 1, "image_path": image_path}]

#         # Ensure API key is set
#         if not OPENAI_API_KEY:
#             raise HTTPException(status_code=500, detail="OpenAI API key is missing in environment variables.")

#         # Set OpenAI API Key
#         openai.api_key = OPENAI_API_KEY

#         for image in images:
#             base64_img = f"data:image/jpeg;base64,{encode_image(image['image_path'])}"

#             # Call OpenAI API for each image
#             response = openai.ChatCompletion.create(
#                 model='gpt-4o',
#                 messages=[
#                     {
#                         "role": "system",
#                         "content": (
#                             "You are an OCR system. Your task is to extract text from images and return it as structured JSON."
#                             " Do not modify the content on your own. Return exactly what is extracted without any changes."
#                         ),
#                     },
#                     {
#                         "role": "user",
#                         "content": [
#                             {"type": "text", "text": "Extract and return the JSON document with data."},
#                             {"type": "image_url", "image_url": {"url": f"{base64_img}"}}
#                         ],
#                     }
#                 ],
#                 max_tokens=1000,
#             )

#             json_data = process_response(response)
#             extracted_data.append({"page": image["page"], "data": json_data})

#         # Save final extracted JSON
#         json_filename = f"{pdf_filename}.json"
#         json_path = os.path.join(DATA_FOLDERS[data_type], json_filename)
#         with open(json_path, "w") as json_file:
#             json.dump(extracted_data, json_file, indent=4)

#         # ✅ Cleanup: Delete all temporary images after processing
#         shutil.rmtree(TEMP_PDF_FOLDER, ignore_errors=True)
#         os.makedirs(TEMP_PDF_FOLDER, exist_ok=True)  # Recreate the folder

#         return {"message": "✅ JSON extracted successfully!", "json_filename": json_filename}

#     except Exception as e:
#         # In case of an error, still ensure cleanup happens
#         shutil.rmtree(TEMP_PDF_FOLDER)
#         os.makedirs(TEMP_PDF_FOLDER, exist_ok=True)  # Recreate the folder

#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, File, UploadFile, HTTPException
import openai
import base64
import json
import os
import re
import shutil
from dotenv import load_dotenv
import uvicorn
import fitz  # PyMuPDF
from io import BytesIO
from PIL import Image

# Load environment variables
load_dotenv()

# Load OpenAI API key from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Ensure necessary folders exist
DATA_FOLDERS = {
    "question": "./Question_data",
    "answer": "./Answer_data"
}
TEMP_PDF_FOLDER = "./pdf_pages"

for folder in DATA_FOLDERS.values():
    os.makedirs(folder, exist_ok=True)
os.makedirs(TEMP_PDF_FOLDER, exist_ok=True)

def encode_image(image_path):
    """Encodes an image file to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_json_from_response(response_content):
    """Extracts valid JSON content from OpenAI's response using regex."""
    try:
        json_match = re.search(r"\{.*\}", response_content, re.DOTALL)
        if json_match:
            json_string = json_match.group(0)  # Extract JSON part
            return json.loads(json_string)  # Convert to dict
        else:
            raise ValueError("No valid JSON found in response.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON structure received from OpenAI.")

def process_response(response):
    """Processes the OpenAI API response and extracts JSON data."""
    response_content = response.choices[0].message.content.strip()
    return extract_json_from_response(response_content)

def convert_pdf_to_images(pdf_bytes, pdf_filename):
    """Converts a PDF file into JPEG images using PyMuPDF (fitz) and saves them in TEMP_PDF_FOLDER."""
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    saved_images = []

    try:
        for i in range(len(pdf_document)):  # Iterate through each page
            page = pdf_document[i]
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            img_filename = f"{pdf_filename}_page_{i+1}.jpeg"
            img_path = os.path.join(TEMP_PDF_FOLDER, img_filename)
            img.save(img_path, format="JPEG")
            saved_images.append({"page": i + 1, "image_path": img_path})
    finally:
        pdf_document.close()  # Ensure the document is closed properly

    return saved_images

def safe_delete_folder(folder_path):
    """Safely deletes a folder and handles permission errors."""
    if os.path.exists(folder_path):  # Ensure folder exists before deletion
        def on_rm_error(func, path, exc_info):
            """Handle permission errors during deletion."""
            try:
                os.chmod(path, 0o777)  # Change permission
                func(path)  # Retry deletion
            except Exception as e:
                print(f"Error deleting {path}: {e}")

        shutil.rmtree(folder_path, onerror=on_rm_error)
        os.makedirs(folder_path, exist_ok=True)  # Recreate after deletion

@app.post("/extract-json/{data_type}")
async def extract_json(data_type: str, file: UploadFile = File(...)):
    """Endpoint to upload an image or PDF and extract JSON using OpenAI.
    - `data_type`: "question" or "answer" (Determines where data is saved)
    """
    if data_type not in DATA_FOLDERS:
        raise HTTPException(status_code=400, detail="Invalid data type. Use 'question' or 'answer'.")

    try:
        # Read file bytes
        file_bytes = await file.read()
        pdf_filename = os.path.splitext(file.filename)[0]

        extracted_data = []  # Store extracted JSON data from all pages

        if file.filename.endswith(".pdf"):
            # Convert PDF to images and save them
            images = convert_pdf_to_images(file_bytes, pdf_filename)
        else:
            # Handle direct image upload
            image_path = os.path.join(TEMP_PDF_FOLDER, f"{pdf_filename}.jpeg")
            with open(image_path, "wb") as f:
                f.write(file_bytes)
            images = [{"page": 1, "image_path": image_path}]

        # Ensure API key is set
        if not OPENAI_API_KEY:
            raise HTTPException(status_code=500, detail="OpenAI API key is missing in environment variables.")

        # Set OpenAI API Key
        openai.api_key = OPENAI_API_KEY

        for image in images:
            base64_img = f"data:image/jpeg;base64,{encode_image(image['image_path'])}"

            # Call OpenAI API for each image
            response = openai.ChatCompletion.create(
                model='gpt-4o',
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an OCR system. Your task is to extract text from images and return it as structured JSON."
                            " Do not modify the content on your own. Return exactly what is extracted without any changes."
                        ),
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Extract and return the JSON document with data."},
                            {"type": "image_url", "image_url": {"url": f"{base64_img}"}}
                        ],
                    }
                ],
                max_tokens=1000,
            )

            json_data = process_response(response)
            extracted_data.append({"page": image["page"], "data": json_data})

        # Save final extracted JSON
        json_filename = f"{pdf_filename}.json"
        json_path = os.path.join(DATA_FOLDERS[data_type], json_filename)
        with open(json_path, "w") as json_file:
            json.dump(extracted_data, json_file, indent=4)

        # ✅ Cleanup: Delete all temporary images after processing
        safe_delete_folder(TEMP_PDF_FOLDER)

        return {"message": "✅ JSON extracted successfully!", "json_filename": json_filename}

    except Exception as e:
        # Ensure cleanup happens even if an error occurs
        safe_delete_folder(TEMP_PDF_FOLDER)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
