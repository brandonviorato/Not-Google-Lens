import ollama
import textwrap

model = "7shi/llama-translate:8b-q4_K_M"

def translate(instruction, input_text):
    prompt = textwrap.dedent(f"""
        ### Instruction:
        {instruction}

        ### Input:
        {input_text}

        ### Response:""").strip()

    messages = [{ "role": "user", "content": prompt }]

    try:
        response = ollama.chat(model=model, messages=messages)
        # print(response)
    except ollama.ResponseError as e:
        print("Error:", e.error)
        return None
    
    response_content = response["message"]["content"].strip()

    return response_content