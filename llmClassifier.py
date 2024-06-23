import threading
import os
import json
import openai
import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

OPENAI_API_KEYS = os.getenv("OPENAI_API_KEYS").split(',')
print(OPENAI_API_KEYS[0])

class DiseaseClassifier:
  def __init__(self, disease, api_key=None):
    self.disease_file = disease+'.json'
    with open(self.disease_file, "r") as fr:
      self.labels = json.load(fr)
    self.client = openai.Client(api_key=api_key)

  def classify(self, msg):
    def response(prompt):
      res = json.loads( self.client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": f"You are a knowledgable assistant, an expert in clinical trials and know important symptoms of diseases.\n\nGiven dictionary of labels: {self.labels} \n and a prompt consisting of a set of patient notes, classify the message and return the label, confidence score, and a one sentence explanation in {{\"label\":__,\"confidence\":__,\"explaination\":__}} json format."},
                            {"role": "user", "content": prompt},],
                        seed=42
                        ).choices[0].message.content)
      res['score'] = np.where(res['label'] == 'Negative', np.around(1.0-res['confidence'], 2), np.around(res['confidence'], 2))
      return res
    ufun_response = np.frompyfunc(response, 1, 1)
    return ufun_response(msg)
  
class BatchDiseaseClassifier:
  def __init__(self, disease, data_file, api_keys):
    self.df = None
    self.load_df(data_file)
    self.disease = disease
    self.threads = [threading.Thread(target=self.worker(api_key)) for api_key in api_keys]

  def load_df(self, data_file):
    self.df = pd.read_csv(data_file)
    self.df['Semaphore'] = 0
    self.df['label'] = None
    self.df['confidence'] = None
    self.df['explanation'] = None
    self.df['score'] = None

  def worker(self, api_key):
    dc = DiseaseClassifier(self.disease, api_key)
    while self.df['label'].count() < self.df['label'].size:
      for i, row in self.df.iterrows():
        if row['Semaphore'] == 0:
          self.df.at[i, 'Semaphore'] = 1
          self.df.loc[i, ['label', 'confidence', 'explanation', 'score']] = dc.classify(row['Patient Notes'])
          # self.df.loc[i, 'score'] = np.where(self.df.loc[i, 'label'] == 'Negative', np.around(1.0-self.df.loc[i, 'confidence'], 2), np.around(self.df.loc[i, 'confidence'], 2))
          print(self.df.loc[i])
          self.df.at[i, 'Semaphore'] = 0

  def classify(self):
    for thread in self.threads:
      thread.start()

    for thread in self.threads:
      thread.join()
    return self.df
  
bdc = BatchDiseaseClassifier('lymphedema', 'patient_data.csv', np.repeat(OPENAI_API_KEYS,10))
# bdc.load_df()
print(bdc.classify())

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
