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

extracted_text = ''

# Extract OCR text
for bbox, text, confidence in results:
    # print(f"{text} (confidence: {confidence:.2f})")
    extracted_text = extracted_text + text + '\n'

# Delete binarized image
os.remove(binarized_image_path)

print('Translating extracted text...')

translation_prompt = load_prompt('translation_prompt.txt')
image_translation = translate(translation_prompt, extracted_text)

print(image_translation)