from dotenv import load_dotenv
load_dotenv()

import os
import logging
from fastapi import FastAPI, HTTPException, Depends, Header
from model import generate_model, predict_hiring, CandidateData

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/generate")
async def generate():
    generate_model()
    return {"message": 'model generated'}

@app.post("/predict")
async def predict(candidate: CandidateData):
    return predict_hiring(candidate)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)