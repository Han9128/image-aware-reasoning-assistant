
import cv2
import pytesseract
import os

def extract_text(img_path):
    
    image = cv2.imread(img_path)
    if image is None:
        raise ValueError(f"Could not open image: {img_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    
    text = pytesseract.image_to_string(gray).strip()

    return {
        "detected_text": text,
        "word_count": len(text.split()) if text else 0,
        "has_text": bool(text)
    }

if __name__ == "__main__":
    
    img_path = "data/watermarkprotection.png"
    
    try:
        res = extract_text(img_path)
        print(f"OCR Analysis: {res}")
    except Exception as e:
        print(f"Error during OCR: {e}")