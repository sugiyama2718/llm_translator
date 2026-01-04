import os
import time
from google import genai
from google.genai import types

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
# Get from environment variables or define directly
API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBDgtO02wioWIF0FBxvFglZiHkWA2tqlKk")
#MODEL_ID = "gemini-3-flash-preview"
MODEL_ID = "gemini-2.5-flash-lite"

# ---------------------------------------------------------
# Client Initialization
# ---------------------------------------------------------
client = genai.Client(api_key=API_KEY)

def translate_ja_to_en(text: str) -> str:
    """
    Translate Japanese to English using Gemini 3 Flash.
    """
    if not text:
        return ""

    start_time = time.time()

    # Fix role as "Translator" via System Instruction (improve speed and accuracy)
    # Pass only the text to translate as user input
    response = client.models.generate_content(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction="You are a professional translator. Translate the following Japanese text into natural English. Output only the translation.",
            temperature=0.1, # Low temperature to prioritize accuracy and speed over creativity
        ),
        contents=text
    )

    end_time = time.time()
    latency = end_time - start_time
    print(f"[Debug] Latency: {latency:.4f} sec")

    return response.text.strip()

# ---------------------------------------------------------
# Execution Test
# ---------------------------------------------------------
if __name__ == "__main__":
    while True:
        user_input = input("Enter Japanese text (q to quit): ")
        if user_input.lower() == 'q':
            break
        
        try:
            english_text = translate_ja_to_en(user_input)
            print(f"English: {english_text}\n")
        except Exception as e:
            print(f"An error occurred: {e}")