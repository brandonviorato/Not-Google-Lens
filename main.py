import ollama
import easyocr

reader = easyocr.Reader(['ja', 'en'])  # e.g., Japanese + English
results = reader.readtext('img/test-1.jpg')

extractedText =''

for bbox, text, confidence in results:
    print(f"{text} (confidence: {confidence:.2f})")
    extractedText += text

def translate(text):
    prompt = f"""
    Task: Translate text from its source language to English. The text you receive will be text that is extracted from an image using OCR. The text will contain a mix of english and the source language. It is your job to examine the text and translate it to English using any context that you can discern from the extracted English text. If there is no English text, then do your best to translate the text so that it is not a literal translation (unless appropriate).
    Guidelines: Ensure translations maintain the meaning and context of the original text. Use proper grammar and vocabulary suitable for native English speakers. Retain the tone and style of the original text (e.g., formal, casual, professional). Handle idiomatic expressions and cultural references appropriately by translating them into equivalent English expressions where possible. If the input text is ambiguous, provide the most likely translation based on context. You must be able to understand, not only the words, but also the semantic context in which they're used. In this way, you will return a more accurate translation of the input phrase or phrases. The grammar rules, formal versus informal, and colloquialisms all need to be considered.
    Input: {text}
    Output: Provide the English translation only. Do not add anything else. Do not stray from this task."""
    response = ollama.chat(model="mistral", messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content']

translatedText = translate(extractedText)

print(translatedText)