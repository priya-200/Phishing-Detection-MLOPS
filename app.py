import sys
import os
import certifi
import pandas as pd
import pymongo
import traceback
import logging

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constants.training_pipeline import (
    DATA_INGESTION_DATABASE_NAME,
    DATA_INGESTION_COLLECTION_NAME
)

from dotenv import load_dotenv
load_dotenv()

# MongoDB Connection
MONGODB_URL = os.getenv("MONGODB_URL")
ca = certifi.where()
client = pymongo.MongoClient(MONGODB_URL, tlsCaFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# FastAPI Setup
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

# Template for HTML rendering
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    """Triggers the training pipeline."""
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful", status_code=200)
    except Exception as e:
        error_trace = traceback.format_exc()
        logging.error(f"Training failed: {str(e)}\n{error_trace}")
        raise NetworkSecurityException(e, sys)

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    """Predict route - accepts a CSV file, processes it, and returns predictions."""
    try:
        # Read file contents for debugging
        contents = await file.read()
        print(contents[:200])  # Print first 200 bytes to verify format
        
        # Reset file pointer before reading with pandas
        file.file.seek(0)

        # Load CSV
        df = pd.read_csv(file.file)

        # Load Model and Preprocessor
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        # Make Predictions
        y_pred = network_model.predict(df)
        df["predicted_column"] = y_pred

        # Save predictions
        df.to_csv("prediction_output/output.csv", index=False)

        # Convert DataFrame to HTML Table
        table_html = df.to_html(classes="table table-striped")
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        error_trace = traceback.format_exc()
        logging.error(f"Prediction failed: {str(e)}\n{error_trace}")
        return Response(f"Error occurred: {str(e)}", status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
