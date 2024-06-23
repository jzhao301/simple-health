import csv
import uvicorn


from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/api/retrieve-top-patients")
async def retrieve_top_patients(request: Request):
    patients_input = await request.json()
    return {"patients": patients_input}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)