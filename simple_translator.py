import os
import time
from google import genai
from google.genai import types

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get from environment variables or raise error if missing
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

#MODEL_ID = "gemini-3-flash-preview"
MODEL_ID = "gemini-2.5-flash-lite"

# ---------------------------------------------------------
# Client Initialization
# ---------------------------------------------------------
client = genai.Client(api_key=API_KEY)

from typing import Generator

def translate_ja_to_en(text: str) -> Generator[str, None, str]:
    """
    Translate Japanese to English using Gemini 3 Flash.
    """
    if not text:
        return ""

    start_time = time.time()

    # Fix role as "Translator" via System Instruction (improve speed and accuracy)
    # Pass only the text to translate as user input
    response = client.models.generate_content_stream(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction="You are a professional translator. Translate the following Japanese text into natural English. Output only the translation.",
            temperature=0.1, # Low temperature to prioritize accuracy and speed over creativity
        ),
        contents=text
    )

    full_text = ""
    for chunk in response:
        if chunk.text:
            yield chunk.text
            full_text += chunk.text

    end_time = time.time()
    latency = end_time - start_time
    # Latency measurement is for the full stream here, or first token? 
    # Usually latency is first token, but here we measure total time after loop.
    # Let's keep it simple for now or adjust if needed.
    print(f"\n[Debug] Total time: {latency:.4f} sec")
    
    return full_text


# ---------------------------------------------------------
# Execution Test
# ---------------------------------------------------------
if __name__ == "__main__":
    while True:
        user_input = input("Enter Japanese text (q to quit): ")
        if user_input.lower() == 'q':
            break
        
        try:
            print("English: ", end="", flush=True)
            full_translation = ""
            for chunk in translate_ja_to_en(user_input):
                 print(chunk, end="", flush=True)
                 full_translation += chunk # Accumulate full translation
            print("\n")

        except Exception as e:
            print(f"An error occurred: {e}")