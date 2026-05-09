from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
import joblib
from sklearn.preprocessing import PolynomialFeatures

# Load model
with open('models/model_3.pkl', 'rb') as f:
    model = pickle.load(f)

torque_model = joblib.load('models/torque_model.joblib')
torque_poly  = joblib.load('models/torque_poly_transformer.joblib')

app = FastAPI()

# Input schema
class PredictInput(BaseModel):
    mass: float
    acceleration: float

class TorqueInput(BaseModel):
    r_m: float
    F_N: float
    theta_deg: float

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

@app.get("/model/torque")
def model_torque_info():
    return {
        "model" : "Linear Regression, Polynomial Regression",
        "version" : "3.0",
        "entity" : "Torque",
        "trained_on": "1000 synthetic data points"
    }

@app.post("/predict/torque")
def predict_torque(data: TorqueInput):
    sine_theta = np.sin(np.radians(data.theta_deg))
    poly = PolynomialFeatures(degree=3)
    X_input = np.array([[data.r_m, data.F_N, sine_theta]])

    X_transformed = torque_poly.transform(X_input)

    torque = torque_model.predict(X_transformed)[0]
    return {
        "Torque" : round(float(torque), 2),
        "unit" : "Nm",
        "formula": "τ = r × F × sin(θ)",
        "inputs": {
            "r_m": data.r_m,
            "F_N": data.F_N,
            "theta_deg": data.theta_deg
        }
    }