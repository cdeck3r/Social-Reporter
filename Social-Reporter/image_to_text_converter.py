from PIL import Image
from pytesseract import pytesseract


def convert(image):
    words = pytesseract.image_to_string(Image.fromarray(image)).strip().split()
    return words