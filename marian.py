import os

from transformers import MarianMTModel, MarianTokenizer
import subprocess
import sys

# Uninstall numpy and scipy
subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "numpy", "scipy", "-y"])

# Install specific version of numpy and latest scipy
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==1.26.4", "scipy", "--no-cache-dir"])

# Upgrade torch, torchvision, transformers, and optree
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "torch", "torchvision", "transformers", "optree"])


def load_model(model_name):
    """Load the tokenizer and model for the given MarianMT model name."""
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return model, tokenizer

def translate(text, model, tokenizer):
    """Translate text using the specified model and tokenizer."""
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    output = model.generate(**inputs)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def translate_and_save(input_file, output_file, model_name, src_lang, dest_lang):
    """Translate lines one by one from input file and save immediately after translation."""
    
    # Skip processing if the translated file already exists
    if os.path.exists(output_file):
        print(f"Skipping translation: {output_file} already exists.")
        return

    model, tokenizer = load_model(model_name)

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line_no, line in enumerate(infile, start=1):
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            
            translated_text = translate(line, model, tokenizer)
            outfile.write(translated_text + '\n')

            print(f"Translated Line {line_no} ({src_lang} → {dest_lang}) and saved to {output_file}")



# Define file paths
# base_path = r"C:\Users\chaud\Downloads\LLM\LLM_dataset"
base_path = os.path.join(os.getcwd(), "LLM_dataset")

original_files = {
    'en': rf"{base_path}\Orignal\eng.devtest",
    'ur': rf"{base_path}\Orignal\ur.devtest",
    'pa': rf"{base_path}\Orignal\pa.devtest",
}
translated_files = {
    'en': {'ur': rf"{base_path}\Translated\marian\eng_to_ur.txt", 'pa': rf"{base_path}\Translated\marian\eng_to_pa.txt"},
    'ur': {'en': rf"{base_path}\Translated\marian\ur_to_eng.txt", 'pa': rf"{base_path}\Translated\marian\ur_to_pa.txt"},
    'pa': {'en': rf"{base_path}\Translated\marian\pa_to_eng.txt", 'ur': rf"{base_path}\Translated\marian\pa_to_ur.txt"},
}

# Define models
translation_models = {
    ('en', 'ur'): "Helsinki-NLP/opus-mt-en-ur",
    ('en', 'pa'): "Helsinki-NLP/opus-mt-en-mul",
    ('ur', 'en'): "Helsinki-NLP/opus-mt-ur-en",
    ('ur', 'pa'): "Helsinki-NLP/opus-mt-ur-mul",
    ('pa', 'en'): "Helsinki-NLP/opus-mt-mul-en",
    ('pa', 'ur'): "Helsinki-NLP/opus-mt-mul-ur",
}

# Process each file
for src_lang, input_file in original_files.items():
    for dest_lang, output_file in translated_files[src_lang].items():
        model_name = translation_models.get((src_lang, dest_lang))
        if model_name:
            translate_and_save(input_file, output_file, model_name, src_lang, dest_lang)

print("\nAll translations completed and saved!")

