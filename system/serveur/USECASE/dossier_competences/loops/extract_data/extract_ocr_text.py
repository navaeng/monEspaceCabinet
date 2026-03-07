import cv2
import fitz
import numpy as np
import pytesseract


def extract_ocr_text(page):
    img = cv2.cvtColor(np.frombuffer(page.get_pixmap(matrix=fitz.Matrix(2, 2)).samples, np.uint8).reshape(page.rect.height*2, page.rect.width*2, -1), cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(cv2.adaptiveThreshold(img, 255, 1, 1, 11, 10), lang="fra+eng", config="--psm 3")