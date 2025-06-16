import easyocr
import cv2
import os

from image_binarizer import binarize
from prompt_loader import load_prompt
from translator import translate

# Select image
image_path = "img/test-1.jpg"
image = cv2.imread(image_path)

binarized_image_path = binarize(image)

print('Extracting text from image...')

# OCR binarized image
reader = easyocr.Reader(['ja', 'en'])  # e.g., Japanese + English
results = reader.readtext(binarized_image_path)

print('Translating extracted text...')

translation_prompt = load_prompt('translation_prompt.txt')

translated_results = []

for bounding_box, text, confidence in results:
    translated_text = translate(translation_prompt, text)
    translated_results.append((bounding_box, translated_text, confidence))

results = translated_results

print(results)

# Delete binarized image
os.remove(binarized_image_path)
