import csv
import uvicorn
import numpy as np
import pandas as pd
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from llmClassifier import BatchDiseaseClassifier, DiseaseClassifier
from diseaseLoader import generate_disease_json

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/api/patient-data")
async def get_patient_data():
    file_path = "patient_data.csv"
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        data = list(reader)
    return {"data": data}

@app.get("/api/load-disease")
async def load_disease(disease: str):
    try:
        generate_disease_json(disease)
        return
    except Exception as e:
        return

@app.get("/api/classify-disease")
async def classify_disease(disease: str, patient_notes: str):
    dc = DiseaseClassifier(disease)
    try:
        return dc.classify(patient_notes)
    except Exception as e:
        return
    
@app.get("/api/disease-keys")
async def get_keys():
    with open('disease_hrefs.json', 'r') as fr:
        return fr.read()

@app.post("/api/retrieve-top-patients")
async def retrieve_top_patients(request: Request):
    input = await request.json()
    clinical_trial_notes = input["input"]
    top_patients = input["topPatientsData"]["topPatientsData"]
    all_patients = input["topPatientsData"]["allPatientsData"]
    OPENAI_API_KEYS = os.getenv("OPENAI_API_KEYS").split(',')
    bdc = BatchDiseaseClassifier('lymphedema', np.repeat(OPENAI_API_KEYS,10))
    all_patients_df = pd.DataFrame()
    all_patients_df = pd.DataFrame(all_patients[1:], columns=all_patients[0])
    bdc.loads_df(all_patients_df)
    bdc.classify()
    return

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)