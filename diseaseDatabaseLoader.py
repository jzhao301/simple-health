from bs4 import BeautifulSoup
import json
import requests

base_url = 'https://www.mayoclinic.org/diseases-conditions/index?letter='
disease_href = {}
for c in range(65,91):
    url = base_url + chr(c)
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if '/diseases-conditions/' in href and '/symptoms-causes/' in href:
            disease_name = href[href.find('/diseases-conditions/')+21:href.find('/symptoms-causes/')]
            disease_href[disease_name] = href

            # print(link.get_text())
            # print()

with open('disease_href.json', 'w') as fw:
    json.dump(disease_href, fw)



# text = ''
# for link in soup.find_all('p'):
#     if 'subscribe' in link.get_text() or 'email' in link.get_text() or 'newsletter' in link.get_text():
#         continue
#     if len(link.get_text()) > 50:
#         text += link.get_text() + '\n\n'


    
