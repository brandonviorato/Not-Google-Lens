import easyocr
import cv2
import os

from image_binarizer import binarize
from prompt_loader import load_prompt
from translator import translate
from overlay_text_boxes import overlay_text_boxes

def translate_image(image_path, image_name):
    # Select image
    image = cv2.imread(image_path)

    binarized_image_path = binarize(image)

    print('Extracting text from image...')

    # OCR binarized image
    reader = easyocr.Reader(['ja', 'en'])  # e.g., Japanese + English
    ocr_results = reader.readtext(binarized_image_path)

    # Delete binarized image
    os.remove(binarized_image_path)

    print('Translating extracted text...')

    translation_prompt = load_prompt('translation_prompt.txt')

    translated_ocr_results = []

    for bounding_box, text, confidence in ocr_results:
        translated_text = translate(translation_prompt, text)
        translated_ocr_results.append((bounding_box, translated_text, confidence))

    # output_path = './out/test-6-translated.jpg'
    split_image_name = image_name.split('.')
    output_path = './out/' + split_image_name[0] + "-translated." + split_image_name[1]

    overlay_text_boxes(image, translated_ocr_results, output_path)

    return output_path
