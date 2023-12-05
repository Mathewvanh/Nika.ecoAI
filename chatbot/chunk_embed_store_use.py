import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        return text

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

def tokenize_pages(pages):
    tokenized_pages = []
    for page in pages:
        tokens = tokenizer.encode(page, truncation=True, max_length=1024)
        tokenized_pages.append(tokens)
    return tokenized_pages

# Example usage
pdf_path = 'testpdf.pdf'  # Replace with your PDF file path
pages = extract_text_from_pdf(pdf_path)
tokenized_pages = tokenize_pages(pages)

from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(pages):
    embeddings = [model.encode(page, convert_to_tensor=True) for page in pages]
    return embeddings

# Assuming 'tokenized_pages' contains the tokenized text of each PDF page
# Convert tokenized pages back to text
pages_text = [tokenizer.decode(page) for page in tokenized_pages]
page_embeddings = embed_text(pages_text)

from sklearn.metrics.pairwise import cosine_similarity

def retrieve_relevant_pages(query, page_embeddings, pages_text, top_k=3):
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = cosine_similarity(
        [query_embedding],
        page_embeddings
    )[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]
    return [(pages_text[i], similarities[i]) for i in top_indices]

# Example usage
query = "methodologies used?"
relevant_pages = retrieve_relevant_pages(query, page_embeddings, pages_text)
for text, score in relevant_pages:
    print("Page:", text)
    print("Score:", score)
    print("---")
