import lamini
import os
import json
from dotenv import load_dotenv




with open(f'disease.json', "r") as fr:
  labels = json.load(fr)

patients = ['I am depressed', 'I am not depressed']

prompt = f'given this dictionary of labels: {labels}, Can you classify the following messages and return the label, corresponding confidence scores, and a one sentence explanation in json format: {patients}'
print(labels)
