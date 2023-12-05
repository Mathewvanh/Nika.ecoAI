import csv
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def clean_text(text):
    """ Utility function to clean and trim text """
    return ' '.join(text.split())


def download_pdf(url, category):
    """ Download a PDF from a given URL and save it in the specified category folder """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to download from {url}")
        return

    # Creating category directory if it doesn't exist
    category_dir = f"downloads/{category}"
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)

    # Extracting filename from URL and saving the file
    filename = url.split('/')[-1] if url.split('/')[-1]else "downloaded_file.pdf"
    if not filename.endswith(".pdf"):
        filename +=".pdf"
    filepath = os.path.join(category_dir, filename)

    with open(filepath, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded {filename} to {category_dir}/")


# Read the CSV file
with open('verra_documents.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        category, url = row

        # Fetch the page content
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage: {url}")
            continue

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the 'Download' link
        download_link = None
        for a_tag in soup.find_all('a'):
            if clean_text(a_tag.get_text()) == "Download":
                download_link = a_tag
                break

        if download_link and download_link.get('href'):
            pdf_url = urljoin(url, download_link['href'])
            download_pdf(pdf_url, category)
        else:
            print(f"No download link found at {url}")

print("All downloads are complete.")
