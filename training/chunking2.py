from transformers import AutoTokenizer
import os

os.environ['HF_API_TOKEN'] = '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'

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

# Load the Llama tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

def chunk_text(text, max_length=1024):  # Adjust max_length as per Llama's limit
    # Tokenize the text and get token ids
    tokens = tokenizer.encode(text)
    chunks = []

    for i in range(0, len(tokens), max_length):
        # Ensure that we don't have an index out of range
        end = min(i + max_length, len(tokens))
        chunk = tokens[i:end]
        # Decode tokens back to text
        chunk_text = tokenizer.decode(chunk)
        chunks.append(chunk_text)

    return chunks

# Assuming you have a directory with text files to be chunked
text_directory = "text_files"
chunked_texts = []

for file_name in os.listdir(text_directory):
    if file_name.endswith('.txt'):
        file_path = os.path.join(text_directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            chunked_texts.extend(chunk_text(text))

# Now chunked_texts contains the chunked text data
