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
with open(f'lymphedema.json', "r") as fr:
  labels = json.load(fr)

patientDf = pd.read_csv('Unstructured_Patient_Data_for_Breast_Cancer_Clinic - Unstructured_Patient_Data_for_Breast_Cancer_Clinic.csv')
patients = patientDf['Patient Notes'].tolist()
prompt = f'given this dictionary of labels: {labels}, Can you classify the following messages and return a list of the corresponding original message, labels, confidence scores, and a one sentence explanation in a \[{{\"message\":__,\"label\":__,\"confidence\":__,\"explaination\":__}}\] json format: {patients}'

response = client.chat.completions.create(
model="gpt-3.5-turbo",
messages=[
    {"role": "system", "content": "You are a knowledgable assistant, an expert in clinical trials and know important symptoms of diseases.\n\nGiven the prompt: 'What are some important symptoms of __?' please provide a list of symptoms that are comma separated."},
    {"role": "user", "content": prompt},]
)

print(response.choices[0].message.content[3:-3])
data = json.loads(response.choices[0].message.content[6:-3])


df = pd.DataFrame.from_dict(data, orient='columns')

df['score'] = np.where(df['label'] == 'Negative', 1.0-df['confidence'], df['confidence'])


print(df)
