# =========================
# IMPORT
# =========================
from fastapi import FastAPI
import joblib
import numpy as np

# =========================
# LOAD MODEL
# =========================
model = joblib.load("../model/fraud_model.pkl")
scaler = joblib.load("../model/scaler.pkl")

# =========================
# INIT APP
# =========================
app = FastAPI()

# =========================
# ROOT
# =========================
@app.get("/")
def home():
    return {"message": "Agent AI Fraud Detection API running"}

# =========================
# PREDICT FRAUD
# =========================
@app.post("/predict")
def predict(data: dict):
    """
    Input:
    {
        "transaction": [30 features]
    }
    """

    tx = data["transaction"]

    if len(tx) != 30:
        return {"error": "Transaction must have 30 features"}

    tx = np.array(tx).reshape(1, -1)
    tx = scaler.transform(tx)

    result = model.predict(tx)

    if result[0] == -1:
        return {
            "fraud": True,
            "message": "🚨 Fraud detected"
        }
    else:
        return {
            "fraud": False,
            "message": "✅ Normal"
        }

# =========================
# OPTIONAL: AUTO GENERATE TRANSACTION
# =========================
@app.get("/simulate")
def simulate():
    tx = np.random.rand(30)

    tx_scaled = scaler.transform(tx.reshape(1, -1))
    result = model.predict(tx_scaled)

    return {
        "transaction": tx.tolist(),
        "fraud": result[0] == -1
    }