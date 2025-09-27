import os
from pdf2image import convert_from_path
import pytesseract
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

# ---------- CONFIGURATION ----------
path = r'C:\Users\jmsal\ubs_data\Financial-Peace-of-Mind\data\Research'

output_folder = os.path.join(os.getcwd(), "OCR_texts")
os.makedirs(output_folder, exist_ok=True)

# If on Windows, specify tesseract manually if needed:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# -----------------------------------


def ocr_page(img, page_num):
    """OCR a single PDF page image. Returns (page_num, text)."""
    text = pytesseract.image_to_string(img, lang="eng")
    return page_num, text


def ocr_pdf(pdf_path, output_txt_path):
    """Extract text from a PDF using OCR (parallel per page, limited workers)."""
    images = convert_from_path(pdf_path)
    text_content = [None] * len(images)

    # Progress bar for pages
    with tqdm(total=len(images), desc=f"Processing {os.path.basename(pdf_path)}", unit="page") as pbar:
        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(ocr_page, img, i) for i, img in enumerate(images)]
            for future in as_completed(futures):
                page_num, text = future.result()
                text_content[page_num] = text
                pbar.update(1)

    # Write pages in correct order
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(text_content))

    return os.path.basename(pdf_path)


def main():
    pdf_files = [f for f in os.listdir(path) if f.lower().endswith(".pdf")]

    # Outer parallelism: multiple PDFs at once
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = []
        for filename in pdf_files:
            pdf_path = os.path.join(path, filename)
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(output_folder, txt_filename)

            futures.append(executor.submit(ocr_pdf, pdf_path, txt_path))

        for future in as_completed(futures):
            try:
                done_file = future.result()
                print(f"\n✅ Finished: {done_file}")
            except Exception as e:
                print(f"\n❌ Error: {e}")

    print("\n🎉 All OCR tasks completed. Texts are saved in:", output_folder)


if __name__ == "__main__":
    main()
