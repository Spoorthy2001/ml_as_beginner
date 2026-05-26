from fastapi import FastAPI
from pydantic import BaseModel, Field
import pickle
import numpy as np
import joblib
from sklearn.preprocessing import PolynomialFeatures

gravitational_constant = 9.81

# Load model
with open('models/model_3.pkl', 'rb') as f:
    model = pickle.load(f)

torque_model = joblib.load('models/torque_model.joblib')
torque_poly = joblib.load('models/torque_poly_transformer.joblib')

energy_model = joblib.load('models/energy_model.joblib')
energy_poly  = joblib.load('models/energy_poly_transformer.joblib')

app = FastAPI()


# Input schema
class PredictInput(BaseModel):
    mass: float
    acceleration: float


class TorqueInput(BaseModel):
    r_m: float = Field(..., ge=0.1, le=1.0)
    F_N: float = Field(..., ge=10, le=500)
    theta_deg: float = Field(..., ge=0, le=360)


class EnergyInput(BaseModel):
    mass_kg: float = Field(..., gt=0, le=5000)
    velocity_ms: float = Field(..., ge=0, le=100)
    height_m: float = Field(..., ge=0, le=1000)


# Health check
@app.get("/")
def root():
    return {"status": "alive", "api": "Hence Proved — F=ma"}


# Model info
@app.get("/model")
def model_info():
    return {
        "model": "Linear Regression",
        "version": "3.0",
        "law": "Newton's Second Law — F = ma",
        "feature": "mass_X_acceleration",
        "trained_on": "500 synthetic data points"
    }


# Prediction
@app.post("/predict")
def predict(data: PredictInput):
    mass_x_acceleration = data.mass * data.acceleration
    force = model.predict([[mass_x_acceleration]])[0]
    return {
        "force": round(float(force), 2),
        "unit": "N",
        "formula": "F = mass × acceleration",
        "inputs": {
            "mass_kg": data.mass,
            "acceleration": data.acceleration
        }
    }


@app.get("/model/torque")
def model_torque_info():
    return {
        "model": "Linear Regression, Polynomial Regression",
        "version": "3.0",
        "entity": "Torque",
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
        "Torque": round(float(torque), 2),
        "unit": "Nm",
        "formula": "τ = r × F × sin(θ)",
        "inputs": {
            "r_m": data.r_m,
            "F_N": data.F_N,
            "theta_deg": data.theta_deg
        }
    }


@app.post("/predict/energy")
def predict_energy(data: EnergyInput):
    half_m_v2 = 0.5 * data.mass_kg * (data.velocity_ms)**2
    mgh = data.mass_kg * gravitational_constant * data.height_m
    X_input = np.array([[half_m_v2, mgh]])
    energy = energy_model.predict(X_input)[0]
    return{
        "energy": round(float(energy), 2),
        "energy_KJ": round(float(energy)/1000, 4),
        "unit": "Joules",
        "formula": "E = ½mv² + mgh",
        "inputs": {
            "mass_kg": data.mass_kg,
            "velocity_ms": data.velocity_ms,
            "height_m": data.height_m
        }

    }
