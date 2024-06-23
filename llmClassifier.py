import lamini
import os
import json
import openai
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.Client()
with open(f'disease.json', "r") as fr:
  labels = json.load(fr)

patients = ['I am depressed', 'I am not depressed']
prompt = f'given this dictionary of labels: {labels}, Can you classify the following messages and return the label, corresponding confidence scores, and a one sentence explanation in json format: {patients}'

response = client.chat.completions.create(
model="gpt-3.5-turbo",
messages=[
    {"role": "system", "content": "You are a knowledgable assistant, an expert in clinical trials and know important symptoms of diseases.\n\nGiven the prompt: 'What are some important symptoms of __?' please provide a list of symptoms that are comma separated."},
    {"role": "user", "content": prompt},]
)

data = json.loads(response.choices[0].message.content)['results']


df = pd.DataFrame.from_dict(data, orient='columns')

df['score'] = np.where(df['label'] == 'Normal', 1.0-df['confidence'], df['confidence'])


print(df)
