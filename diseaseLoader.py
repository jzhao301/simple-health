from bs4 import BeautifulSoup
from openai import OpenAI
import requests

# URL of the page to scrape
url = 'https://www.mayoclinic.org/diseases-conditions/atrial-fibrillation/symptoms-causes/syc-20350624'

oaiClient = OpenAI()
# Fetch the HTML content
response = requests.get(url)
html_content = response.text

# Create a Beautiful Soup object
soup = BeautifulSoup(html_content, 'html.parser')

# Find all links and print them
for link in soup.find_all('p'):
    if 'subscribe' in link.get_text() or 'email' in link.get_text() or 'newsletter' in link.get_text():
        continue
    if len(link.get_text()) > 50:
        print(link.get_text())
    
