import os
import re
from transformers import GPT2Tokenizer

text_directory = "text_files"
chunk_directory = "chunks"

# Initialize the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def find_table_of_contents(text):
    toc_pattern = r"(\d+\.\d+|\d+)\s+([\w\s]+)"
    return re.findall(toc_pattern, text)

def find_subsection_split_points(text):
    return [match.start() for match in re.finditer(r"\n\d+(\.\d+)*\s+", text)]

def split_section(section_text, min_tokens=100):
    subsection_points = find_subsection_split_points(section_text)
    split_points = [0]
    accumulated_text = ""

    for point in subsection_points:
        chunk = section_text[split_points[-1]:point]
        accumulated_text += chunk
        if len(tokenizer.encode(accumulated_text)) >= min_tokens:
            split_points.append(point)
            accumulated_text = ""  # Reset for next chunk

    split_points.append(len(section_text))  # Ensure the last part of the section is included
    return split_points

def chunk_text(text, filename, category):
    toc_entries = find_table_of_contents(text)
    start_points = find_subsection_split_points(text)

    category_chunk_dir = os.path.join(chunk_directory, category)
    if not os.path.exists(category_chunk_dir):
        os.makedirs(category_chunk_dir)

    for i, toc_entry in enumerate(toc_entries):
        start = start_points[i] if i < len(start_points) else start_points[-1]
        end = start_points[i+1] if i+1 < len(start_points) else len(text)
        section_text = text[start:end]

        split_points = split_section(section_text)
        for j in range(len(split_points) - 1):
            chunk = section_text[split_points[j]:split_points[j+1]]
            token_count = len(tokenizer.encode(chunk))
            if token_count > 50:  # Save only if token count is more than 50
                chunk_filename = f"{filename}_Section_{toc_entry[0]}_{j+1}.txt"
                chunk_path = os.path.join(category_chunk_dir, chunk_filename)
                with open(chunk_path, 'w', encoding='utf-8') as chunk_file:
                    chunk_file.write(chunk.strip())
                print(f"Created chunk: {chunk_filename}, Token count: {token_count}")

# Process each text file
for category in os.listdir(text_directory):
    category_dir = os.path.join(text_directory, category)
    if os.path.isdir(category_dir):
        for text_file in os.listdir(category_dir):
            if text_file.endswith(".txt"):
                text_path = os.path.join(category_dir, text_file)
                with open(text_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    chunk_text(text, text_file.replace('.txt', ''), category)
