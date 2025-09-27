#from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
#from llama_index.core.agent.workflow import FunctionAgent
#from llama_index.llms.openai import OpenAI
#import asyncio
import os
from pdf2image import convert_from_path
import pytesseract

# ---------- CONFIGURATION ----------
# Change this to the folder containing your PDFs
path = r'C:\Users\jmsal\ubs_data\Financial-Peace-of-Mind\data\Research'

# Output folder for OCR text files
output_folder = os.path.join(os.getcwd(), "OCR_texts")
os.makedirs(output_folder, exist_ok=True)

# If on Windows, you may need to specify the tesseract path explicitly:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# -----------------------------------

def ocr_pdf(pdf_path, output_txt_path):
    """Extract text from a PDF using OCR and save to a text file."""
    text_content = []

    # Convert each PDF page to an image
    images = convert_from_path(pdf_path)

    for i, img in enumerate(images):
        # Run OCR on each page image
        text = pytesseract.image_to_string(img, lang="eng")
        text_content.append(text)

    # Write combined OCR output to text file
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(text_content))


# Process all PDFs in the folder
for filename in os.listdir(path):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(path, filename)
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_path = os.path.join(output_folder, txt_filename)

        print(f"Processing: {filename}")
        ocr_pdf(pdf_path, txt_path)

print("✅ OCR completed. Extracted texts are saved in:", output_folder)


