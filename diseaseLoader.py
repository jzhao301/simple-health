import openai
import json
import os
# from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

with open('disease_href.json', 'r') as fr:
  disease_href = json.load(fr)

def generate_disease_json(disease):
    client = openai.Client()
    href = disease_href[disease]
    res_raw = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": f"You are a knowledgable assistant, an expert in clinical trials and know important symptoms of diseases.\n\nGiven s link to a page on Mayo Clinic can you generate a detailed description of symptoms of the disease and a detailed description of a normal person that does not have this disease in {{\"Positive\":str,\"Negative\":str}} json format."},
                            {"role": "user", "content": href},],
                        seed=42
                        ).choices[0].message.content
  
    if '```json' in res_raw:
        res_raw = res_raw[res_raw.find('```json')+7:res_raw.find('```', res_raw.find('```json')+7)]
    response = json.loads(res_raw)
    with open(f'{disease}.json', 'w') as fw:
        json.dump(response, fw)


def main():
    i = 0
    for disease in disease_href.keys():
        generate_disease_json(disease)
        if i > 5:
            break
        i += 1

if __name__ == '__main__':
    main()