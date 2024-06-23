from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()
app.debug = True
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def my_middleware(app):
    def middleware(environ, start_response):
        response = app(environ, start_response)

        headers = [
            ("Access-Control-Allow-Origin", "*"),
            ("Access-Control-Allow-Headers", "*"),
            ("X-foo", "bar"),
        ]
        new_response = []
        for name, value in response:
            if name.lower() != "content-length":
                new_response.append((name, value))
        new_response.extend(headers)

        return new_response

    return middleware

@app.get("/api")
async def read_root():
    return {"Hello": "World"}

@app.post("/api/retrieve-top-patients")
async def retrieve_top_patients(request: Request):
    patients_input = await request.json()
    return {"patients": patients_input}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)