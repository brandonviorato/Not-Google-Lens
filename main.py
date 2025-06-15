import ollama
import easyocr
import cv2
import os

from prompt_loader import load_prompt

# Select image
image_path = "img/test-1.jpg"
image = cv2.imread(image_path)

# Pre-process image through binarization (make grayscale)
def binarize(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    storage_path = "temp/gray.jpg"
    cv2.imwrite(storage_path, gray_image)
    return storage_path

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

# Load context prompt
context_prompt = load_prompt('context_prompt.txt')

print('Generating image context...')

# Generate image context
context_response = ollama.chat(
    model='llama3.2-vision',
    messages=[{
        'role': 'user',
        'content': context_prompt,
        'images': [image_path]
    }]
)

image_context = context_response['message']['content'].strip()

# Load translation prompt
context_prompt = load_prompt('translation_prompt.txt')

print('Translating extracted text...')

# Generate image translation
translation_response = ollama.chat(
    model='7shi/llama-translate:8b-q4_K_M',
    messages=[{
        'role': 'user',
        'content': context_prompt + '\n' + image_context + '\n' + '### Input:' + '\n' + extracted_text + '\n' + '### Response:',
    }]
)

image_translation = translation_response['message']['content'].strip()

print(image_translation)