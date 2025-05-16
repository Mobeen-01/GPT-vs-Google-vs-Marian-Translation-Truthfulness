import os
import subprocess
import sys

# Install required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "openai", "httpx"])
import openai
from difflib import SequenceMatcher

# Define base path dynamically
base_path = os.path.join(os.getcwd(), "LLM_dataset")
original_path = os.path.join(base_path, "Orignal")
translated_path = os.path.join(base_path, "Translated", "gpt")
os.makedirs(translated_path, exist_ok=True)  # Ensure output directory exists

# Function to load dataset lines
def load_lines(file_path):
    print(f"Opening dataset: {file_path}")  # Log file opening
    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()

# Load original datasets
eng_lines = load_lines(os.path.join(original_path, "eng.devtest"))
pa_lines = load_lines(os.path.join(original_path, "pa.devtest"))
ur_lines = load_lines(os.path.join(original_path, "ur.devtest"))

# API Key (Replace with your actual API key)
api_key = "your-api-key-here"
client = openai.OpenAI(api_key=api_key)

# Function to translate text
def translate_text(text, target_language):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": f"Translate this to {target_language}: {text}"}]
    )
    return response.choices[0].message.content.strip()

# Function to compute similarity
def calculate_similarity(original, translated):
    return SequenceMatcher(None, original, translated).ratio()

# Function to translate and save line by line
def batch_translate(lines, target_language, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for i, line in enumerate(lines):
            translated = translate_text(line, target_language)
            f.write(translated + "\n")  # Save translation immediately
            print(f"Translated line {i + 1}/{len(lines)} to {target_language} and saved.")

print("Starting translations and saving in real-time...")

# Perform translations and save
batch_translate(eng_lines, "Urdu", os.path.join(translated_path, "eng_to_ur.txt"))
batch_translate(eng_lines, "Punjabi (Gurmukhi script)", os.path.join(translated_path, "eng_to_pa.txt"))
batch_translate(ur_lines, "English", os.path.join(translated_path, "ur_to_eng.txt"))
batch_translate(ur_lines, "Punjabi (Gurmukhi script)", os.path.join(translated_path, "ur_to_pa.txt"))
batch_translate(pa_lines, "English", os.path.join(translated_path, "pa_to_eng.txt"))
batch_translate(pa_lines, "Urdu", os.path.join(translated_path, "pa_to_ur.txt"))

print("All translations completed and saved line by line.")
