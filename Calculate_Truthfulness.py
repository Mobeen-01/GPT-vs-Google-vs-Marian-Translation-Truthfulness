import os
import pandas as pd
import subprocess
import sys


# List of required packages
packages = ["sentence-transformers", "transformers", "torch"]

# Install each package
for package in packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

from sentence_transformers import SentenceTransformer, util

# Load SBERT model for meaning-based similarity
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# Paths
ORIGINAL_PATH = "LLM_dataset/Orignal"
TRANSLATED_PATH = "LLM_dataset/Translated"

# Function to read files
def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

# Load original text files
original_texts = {}
for file in os.listdir(ORIGINAL_PATH):
    if file.endswith(".devtest"):
        lang = file.split(".")[0]  # Extract language name from filename
        original_texts[lang] = read_file(os.path.join(ORIGINAL_PATH, file))

# Process each translation model
for model_name in os.listdir(TRANSLATED_PATH):
    model_path = os.path.join(TRANSLATED_PATH, model_name)
    
    if os.path.isdir(model_path):  # Ensure it's a directory
        print(f"\nProcessing translations for model: {model_name}...")

        results_dict = {}  # Store truthfulness scores for each language pair

        for file in os.listdir(model_path):
            if file.endswith(".txt"):
                lang_pair = file.replace(".txt", "")  # Extract language pair (e.g., "eng_to_ur")
                print(f"Processing file: {lang_pair}")

                # Try to split based on '_to_' for typical language pair formats
                try:
                    src_lang, tgt_lang = lang_pair.split("_to_")
                except ValueError:
                    print(f"Skipping file {file} due to incorrect language pair format.")
                    continue  # Skip files that cannot be processed due to name format

                print(f"Processing file {file} with source language '{src_lang}' and target language '{tgt_lang}'")

                # Proceed with processing if original texts are available
                if src_lang in original_texts:
                    original_lines = original_texts[src_lang]
                    translated_lines = read_file(os.path.join(model_path, file))

                    # Ensure line-by-line comparison
                    min_len = min(len(original_lines), len(translated_lines))
                    similarities = []

                    print(f"  - Processing {lang_pair}: {min_len} lines...")

                    for i in range(min_len):
                        # Compute semantic similarity score
                        score = util.cos_sim(
                            model.encode(original_lines[i], convert_to_tensor=True),
                            model.encode(translated_lines[i], convert_to_tensor=True)
                        ).item()
                        similarities.append(score)

                        # Print score update every 100 lines
                        if (i + 1) % 100 == 0:
                            print(f"    Processed {i + 1} lines...")

                    # Store truthfulness scores
                    results_dict[lang_pair] = similarities

       # Save results to an Excel file
        output_file = os.path.join(model_path, f"{model_name}_truthfulness.xlsx")
        df = pd.DataFrame(results_dict)

        # Calculate & append average truthfulness
        avg_scores = df.mean().to_dict()  # Compute column-wise average
        avg_scores_row = {col: round(avg_scores[col], 4) for col in df.columns}
        avg_scores_row[''] = 'Average Truthfulness'  # Label in the first column

        avg_scores_row_df = pd.DataFrame([avg_scores_row])

        df = pd.concat([df, avg_scores_row_df], ignore_index=True)  # Append as last row
        df.to_excel(output_file, index=False)

        print(f"\nSaved results to {output_file}")

