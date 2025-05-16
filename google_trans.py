import os
import subprocess
import sys

# Install googletrans if not installed
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "googletrans==4.0.0-rc1"])
from googletrans import Translator

# Set base path dynamically
base_path = os.path.join(os.getcwd(), "LLM_dataset")
original_path = os.path.join(base_path, "Orignal")
translated_path = os.path.join(base_path, "Translated", "googletrans")

# Ensure translated directory exists
os.makedirs(translated_path, exist_ok=True)

def load_lines(file_path):
    """Read lines from a file and return as a list."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def save_lines(file_path, lines):
    """Save lines to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def translate_text(text, src_lang, dest_lang):
    """Translate text using Google Translator."""
    translator = Translator()
    try:
        translated = translator.translate(text, src=src_lang, dest=dest_lang)
        return translated.text
    except Exception as e:
        return f"Error: {str(e)}"

def process_translation(src_lines, src_lang, dest_lang, output_file):
    """Translate line-by-line and print progress."""
    translated_lines = []
    
    for i, line in enumerate(src_lines, start=1):
        translated_text = translate_text(line.strip(), src_lang, dest_lang)
        translated_lines.append(translated_text + '\n')
        
        # Print the progress
        print(f"Line {i}: {src_lang.upper()} → {dest_lang.upper()} | Saved to {output_file}")
    
    save_lines(output_file, translated_lines)

# File Paths
def get_file_path(filename):
    return os.path.join(original_path, filename)

# Load original lines
eng_lines = load_lines(get_file_path("eng.devtest"))
punjabi_lines = load_lines(get_file_path("pa.devtest"))
urdu_lines = load_lines(get_file_path("ur.devtest"))

def get_output_path(filename):
    return os.path.join(translated_path, filename)

# Process translations and save
process_translation(eng_lines, 'en', 'ur', get_output_path("eng_to_ur.txt"))
process_translation(eng_lines, 'en', 'pa', get_output_path("eng_to_pa.txt"))
process_translation(urdu_lines, 'ur', 'en', get_output_path("ur_to_eng.txt"))
process_translation(urdu_lines, 'ur', 'pa', get_output_path("ur_to_pa.txt"))
process_translation(punjabi_lines, 'pa', 'en', get_output_path("pa_to_eng.txt"))
process_translation(punjabi_lines, 'pa', 'ur', get_output_path("pa_to_ur.txt"))

print("\n✅ Translation completed and saved successfully!")

