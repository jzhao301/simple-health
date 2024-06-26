import csv
import uvicorn
import numpy as np
import pandas as pd
import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
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
    print(patient_notes)
    try:
        classification = dc.classify(str(patient_notes))
        print(type(classification))
        print(classification)
        # print(json.dumps(classification))
        json_str = json.dumps(classification, indent=4, default=str)

        return Response(content=json_str, media_type='application/json')
    except Exception as e:
        return e
    
@app.get("/api/disease-keys")
async def get_keys():
    with open('disease_href.json', 'r') as fr:
        return fr.read()

@app.post("/api/retrieve-top-patients")
async def retrieve_top_patients(request: Request):
    input = await request.json()
    clinical_trial_notes = input["input"]
    top_patients = input["topPatientsData"]
    all_patients = input["allPatientsData"]
    OPENAI_API_KEYS = os.getenv("OPENAI_API_KEYS").split(',')
    bdc = BatchDiseaseClassifier('lymphedema', np.repeat(OPENAI_API_KEYS,10))
    all_patients_df = pd.DataFrame()
    all_patients_df = pd.DataFrame(all_patients[1:15], columns=all_patients[0])
    bdc.loads_df(all_patients_df)
    result = bdc.classify()
    out = result.copy()
    out["explanation"] = out["explanation"].astype(str)
    out = out[out["label"] == "Positive"]
    column_names = list(out.columns)
    values = out.values
    result = []
    for value in values:
        lst = []
        for v in value:
            lst.append(str(v))
        result.append(lst)
    result.insert(0, column_names)
    return {"data": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)