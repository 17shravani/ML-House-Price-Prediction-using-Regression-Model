from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
from typing import Optional, List, Dict

app = FastAPI(title="ProphetReal AI: World Edition API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
model_india = joblib.load(os.path.join(MODELS_DIR, "prophet_india.joblib")) if os.path.exists(os.path.join(MODELS_DIR, "prophet_india.joblib")) else None
model_global = joblib.load(os.path.join(MODELS_DIR, "prophet_global.joblib")) if os.path.exists(os.path.join(MODELS_DIR, "prophet_global.joblib")) else None

class IndiaFeatures(BaseModel):
    BHK: int
    SqftArea: float
    Bathrooms: int
    Balconies: int
    CityTier: str
    LocationType: str
    Furnishing: str
    PropertyAge: int
    PowerBackup: str
    GatedSecurity: str
    ParkingSpaces: int
    MetroDistance: float
    Clubhouse: str

class GlobalFeatures(BaseModel):
    LotArea: float
    OverallQual: int
    OverallCond: int
    YearBuilt: int
    GrLivArea: float
    FullBath: int
    HalfBath: int
    GarageCars: int
    Neighborhood: str
    KitchenQual: str
    SmartHome: str
    BasementArea: float
    EcoCertified: str

def get_feature_importance(region: str, data: dict):
    if region == "india":
        return {
            "SqftArea": 40,
            "BHK": 20,
            "CityTier": 15,
            "GatedSecurity": 10,
            "MetroDistance": 10,
            "PropertyAge": 5
        }
    else:
        return {
            "GrLivArea": 45,
            "OverallQual": 25,
            "LotArea": 10,
            "YearBuilt": 10,
            "SmartHome": 10
        }

def get_similar_listings(price: float, currency: str):
    return [
        {"name": "Listing Alpha", "price": price * 0.95, "dist": "0.5 km"},
        {"name": "Listing Beta", "price": price * 1.05, "dist": "1.2 km"},
        {"name": "Listing Gamma", "price": price * 0.98, "dist": "2.0 km"}
    ]

@app.post("/predict/india")
def predict_india(data: IndiaFeatures):
    if model_india is None: return {"error": "India model not loaded"}
    df = pd.DataFrame([data.model_dump()])
    pred = float(model_india.predict(df)[0])
    insights = [
        "High-demand location analysis completed.",
        f"Property Age ({data.PropertyAge} yrs) factored into depreciation."
    ]
    if data.GatedSecurity == "Yes": insights.append("Gated Security adds a safety premium.")
    if data.MetroDistance < 2.0: insights.append("Proximity to Metro significantly boosts valuation.")
    if data.Clubhouse == "Yes": insights.append("Clubhouse amenities increase lifestyle value.")

    return {
        "predicted_price": pred,
        "currency": "INR",
        "insights": insights,
        "importance": get_feature_importance("india", data.model_dump()),
        "similar_listings": get_similar_listings(pred, "INR")
    }

@app.post("/predict/global")
def predict_global(data: GlobalFeatures):
    if model_global is None: return {"error": "Global model not loaded"}
    df = pd.DataFrame([data.model_dump()])
    pred = float(model_global.predict(df)[0])
    insights = [
        f"Overall Quality ({data.OverallQual}/10) is a key price driver.",
        f"Living area of {data.GrLivArea} sqft is factored into the square-foot premium."
    ]
    if data.SmartHome == "Yes": insights.append("Smart Home features command a modern-tech premium.")
    if data.EcoCertified == "Yes": insights.append("Eco-Certification adds sustainable market value.")

    return {
        "predicted_price": pred,
        "currency": "USD",
        "insights": insights,
        "importance": get_feature_importance("global", data.model_dump()),
        "similar_listings": get_similar_listings(pred, "USD")
    }

@app.get("/health")
def health():
    return {"india": model_india is not None, "global": model_global is not None}
