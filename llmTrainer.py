# from lamini import LaminiClassifier
import lamini
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

lamini.api_key = os.getenv("LAMINI_API_KEY")
with open(f'disease.json', "r") as fr:
  labels = json.load(fr)

llm = lamini.LaminiClassifier()

for label in labels.keys():
  llm.add_class(label)

for label in labels.keys():
  llm.add_data_to_class(label, labels[label])

llm.train()
llm.save_local("disease.lamini")
