from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# Load model
with open('model_3.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

# Input schema
class PredictInput(BaseModel):
    mass: float
    acceleration: float

# Health check
@app.get("/")
def root():
    return {"status": "alive", "api": "Hence Proved — F=ma"}

# Model info
@app.get("/model")
def model_info():
    return {
        "model"      : "Linear Regression",
        "version"    : "3.0",
        "law"        : "Newton's Second Law — F = ma",
        "feature"    : "mass_X_acceleration",
        "trained_on" : "500 synthetic data points"
    }

# Prediction
@app.post("/predict")
def predict(data: PredictInput):
    mass_x_acceleration = data.mass * data.acceleration
    force = model.predict([[mass_x_acceleration]])[0]
    return {
        "force"  : round(float(force), 2),
        "unit"   : "N",
        "formula": "F = mass × acceleration",
        "inputs" : {
            "mass_kg"       : data.mass,
            "acceleration"  : data.acceleration
        }
    }