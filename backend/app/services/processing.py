import pytesseract
from pdf2image import convert_from_path
import os

def extract_text_from_pdf(pdf_path: str):
    """
    Extract text from PDF file using OCR on images of each page.
    Returns extracted text and a boolean flag indicating OCR usage.
    """
    try:
        # Convert PDF pages to images
        pages = convert_from_path(pdf_path)
        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page)
        used_ocr = True
        return text, used_ocr
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
        return "", False

def extract_text_from_image(image_path: str):
    """
    Extract text from an image file using OCR.
    """
    try:
        text = pytesseract.image_to_string(image_path)
        return text
    except Exception as e:
        print(f"Error extracting text from image {image_path}: {e}")
        return ""
