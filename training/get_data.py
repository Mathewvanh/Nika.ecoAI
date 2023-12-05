import requests
from bs4 import BeautifulSoup
import csv

def clean_text(text):
    """ Utility function to clean and trim text """
    return ' '.join(text.split())
def correct_url(link):
    base_url = "https://verra.org"
    exception_url = "https://verra.org/methodologies"
    if link.startswith(exception_url):
        return link
    else:
        return base_url+link
# URL of the main page
url = "https://verra.org/methodologies-main/"

response = requests.get(url)
if response.status_code != 200:
    print("Failed to retrieve the webpage")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

# Categories to look for
categories = ["PROJECT METHODOLOGIES", "PROJECT MODULES", "PROJECT TOOLS", "JNR MODULES AND TOOLS"]

# Dictionary to hold the links for each category
category_links = {category: [] for category in categories}

# Find the categories
for category in categories:
    # Search each h3 for the required span
    for h3 in soup.find_all('h3'):
        span = h3.find('span', text=lambda text: text and clean_text(text) == category)
        if span:
            div = h3.find_next_sibling('div')
            if div:
                for p_tag in div.find_all('p'):
                    a_tag = p_tag.find('a')
                    if a_tag and a_tag.get('href'):
                        full_link = correct_url(a_tag['href'].strip())
                        category_links[category].append(full_link)
            break  # Break the loop once the category is found

# Writing to CSV
with open('verra_documents.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Category', 'URL'])

    for category, links in category_links.items():
        for link in links:
            writer.writerow([category, link])

print("CSV file has been created with the document links.")
