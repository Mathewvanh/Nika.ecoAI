from pdfminer.high_level import extract_text
import os


def convert_pdf_to_text(pdf_path):
    text = extract_text(pdf_path)
    return text


pdf_directory = "downloads"  # Adjust to your PDF directory path
text_directory = "text_files"

# Create directory for text files if it doesn't exist
if not os.path.exists(text_directory):
    os.makedirs(text_directory)

# Convert all PDFs in the directory to text
for category in os.listdir(pdf_directory):
    category_dir = os.path.join(pdf_directory, category)
    if os.path.isdir(category_dir):
        # Create subdirectory for each category in text_files if it doesn't exist
        text_category_dir = os.path.join(text_directory, category)
        if not os.path.exists(text_category_dir):
            os.makedirs(text_category_dir)

        for pdf_file in os.listdir(category_dir):
            if pdf_file.endswith(".pdf"):
                pdf_path = os.path.join(category_dir, pdf_file)
                text = convert_pdf_to_text(pdf_path)
                text_filename = pdf_file.replace('.pdf', '.txt')
                text_path = os.path.join(text_category_dir, text_filename)

                # Write text to a file
                with open(text_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)
                print(f"Converted {pdf_file} to text.")
