import lamini
import os
import json
import openai
import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class DiseaseClassifier:
  def __init__(self, disease):
    self.disease_file = disease+'.json'
    with open(self.disease_file, "r") as fr:
      self.labels = json.load(fr)
    self.client = openai.Client()

  def classify(self, msg):
    def response(prompt):
      res = json.loads( self.client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": f"You are a knowledgable assistant, an expert in clinical trials and know important symptoms of diseases.\n\nGiven dictionary of labels: {self.labels} \n and a prompt consisting of a set of patient notes, classify the message and return the label, confidence score, and a one sentence explanation in {{\"label\":__,\"confidence\":__,\"explaination\":__}} json format."},
                            {"role": "user", "content": prompt},]
                        ).choices[0].message.content)
      res['score'] = np.where(res['label'] == 'Negative', np.around(1.0-res['confidence'], 2), np.around(res['confidence'], 2))
      return res
    ufun_response = np.frompyfunc(response, 1, 1)
    return ufun_response(msg)
  
class BatchDiseaseClassifier:
  def __init__(self, dc: DiseaseClassifier):
    self.dc = dc
    self.data = None

  def load(self, data_file):
    self.data = pd.read_csv(data_file)

  def loads(self, df):
    self.data = df

  def iterate(self):
    for msg in self.data:
      yield self.dc.classify(msg['Patient Notes'])

# DISEASE_FILE = 'lymphedema.json'



# client = openai.Client()
# with open(DISEASE_FILE, "r") as fr:
#   labels = json.load(fr)

# df = pd.read_csv('Unstructured_Patient_Data_for_Breast_Cancer_Clinic - Unstructured_Patient_Data_for_Breast_Cancer_Clinic.csv')[:2]
# df['prompt'] = f'given this dictionary of labels: {labels}, Can you classify the following messages and return the label, confidence score, and a one sentence explanation in {{\"message\":__,\"label\":__,\"confidence\":__,\"explaination\":__}} json format: {df["Patient Notes"]}'
# patients = patientDf['Patient Notes'].tolist()
# prompt = f'given this dictionary of labels: {labels}, Can you classify the following messages and return a list of the corresponding original message, labels, confidence scores, and a one sentence explanation in a {{\"message\":__,\"label\":__,\"confidence\":__,\"explaination\":__}} json format: {patients}'

# response = np.frompyfunc(lambda prompt: client.chat.completions.create(
# model="gpt-3.5-turbo",
# messages=[
#     {"role": "system", "content": f"You are a knowledgable assistant, an expert in clinical trials and know important symptoms of diseases.\n\nGiven dictionary of labels: {labels} \n and a prompt consisting of a set of patient notes, classify the message and return the label, confidence score, and a one sentence explanation in {{\"label\":__,\"confidence\":__,\"explaination\":__}} json format."},
#     {"role": "user", "content": prompt},]
# ).choices[0].message.content, 1, 1)

# # print(df['prompt'])

# dc = DiseaseClassifier('lymphedema')
# # print(dc.classify(df['Patient Notes']).to_list())

# df = pd.concat([df, pd.DataFrame(dc.classify(df['Patient Notes']).to_list())], axis=1)
# # df.append(dc.classify(df['Patient Notes']))

# # print(df['response'])

# # df['label'] = df['response']['label']
# # df['confidence'] = df['response']['confidence']
# # df['explanation'] = df['response']['explanation']


# # df['response'] = df['response'][df['response'].find('{'):df['response'].find('}')]


# # df = pd.DataFrame.from_dict(data, orient='columns')
# print(df)
# # df['score'] = np.where(df['label'] == 'Negative', 1.0-df['confidence'], df['confidence'])
# # print(df[0])   


# print(df)
