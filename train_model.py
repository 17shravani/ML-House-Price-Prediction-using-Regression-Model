import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import xgboost as xgb
import joblib
import os

def train_india_model():
    print("Generating enhanced Indian real estate dataset...")
    np.random.seed(42)
    n_samples = 3000
    
    bhk = np.random.choice([1, 2, 3, 4, 5, 6], p=[0.05, 0.35, 0.35, 0.15, 0.05, 0.05], size=n_samples)
    sqft_area = (bhk * np.random.normal(550, 120, n_samples)).clip(350, 6000)
    bathrooms = np.where(bhk > 2, np.random.randint(2, 6, n_samples), np.random.randint(1, 3, n_samples))
    balconies = np.random.randint(0, 5, n_samples)
    city_tier = np.random.choice(["Tier 1 (Metro)", "Tier 2", "Tier 3"], p=[0.5, 0.3, 0.2], size=n_samples)
    location_type = np.random.choice(["City Center", "Suburbs", "Outskirts", "Tech Park"], size=n_samples)
    furnishing = np.random.choice(["Unfurnished", "Semi-Furnished", "Fully Furnished"], size=n_samples)
    property_age = np.random.randint(0, 30, n_samples)
    power_backup = np.random.choice(["Yes", "No"], p=[0.8, 0.2], size=n_samples)
    
    # Premium India Features
    gated_security = np.random.choice(["Yes", "No"], p=[0.6, 0.4], size=n_samples)
    parking_spaces = np.random.randint(0, 4, n_samples)
    metro_distance = np.random.uniform(0.1, 15.0, n_samples)
    clubhouse = np.random.choice(["Yes", "No"], p=[0.4, 0.6], size=n_samples)

    price = sqft_area * 5500
    price *= np.array([{"Tier 1 (Metro)": 2.8, "Tier 2": 1.3, "Tier 3": 0.85}[c] for c in city_tier])
    price *= np.array([{"City Center": 1.6, "Tech Park": 1.4, "Suburbs": 1.0, "Outskirts": 0.7}[l] for l in location_type])
    price += (bhk * 600000) + (bathrooms * 250000) - (property_age * 120000)
    price = np.where(furnishing == "Fully Furnished", price + 1200000, price)
    price = np.where(power_backup == "Yes", price + 400000, price)
    price = np.where(gated_security == "Yes", price + 800000, price)
    price = np.where(clubhouse == "Yes", price + 600000, price)
    price += (parking_spaces * 300000)
    price -= (metro_distance * 100000) # Further from metro = lower price
    
    price += np.random.normal(0, 600000, n_samples)
    price = price.clip(1200000, None)

    df = pd.DataFrame({
        "BHK": bhk, "SqftArea": sqft_area, "Bathrooms": bathrooms, "Balconies": balconies,
        "CityTier": city_tier, "LocationType": location_type, "Furnishing": furnishing,
        "PropertyAge": property_age, "PowerBackup": power_backup,
        "GatedSecurity": gated_security, "ParkingSpaces": parking_spaces,
        "MetroDistance": metro_distance, "Clubhouse": clubhouse,
        "SalePrice": price
    })

    X = df.drop(columns=["SalePrice"])
    y = df["SalePrice"]
    
    NUM = ["BHK", "SqftArea", "Bathrooms", "Balconies", "PropertyAge", "ParkingSpaces", "MetroDistance"]
    CAT = ["CityTier", "LocationType", "Furnishing", "PowerBackup", "GatedSecurity", "Clubhouse"]
    
    preprocessor = ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), NUM),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("ohe", OneHotEncoder(handle_unknown="ignore"))]), CAT)
    ])
    
    model = Pipeline([("preprocessor", preprocessor), ("xgb", xgb.XGBRegressor(n_estimators=300, max_depth=6, learning_rate=0.04))])
    model.fit(X, y)
    joblib.dump(model, "models/prophet_india.joblib")
    print("Enhanced India model saved.")

def train_global_model():
    print("Generating enhanced Global real estate dataset...")
    np.random.seed(88)
    n_samples = 3000
    
    lot_area = np.random.gamma(shape=2, scale=6000, size=n_samples).clip(2000, 60000)
    overall_qual = np.random.randint(1, 11, n_samples)
    overall_cond = np.random.randint(1, 11, n_samples)
    year_built = np.random.randint(1950, 2025, n_samples)
    gr_liv_area = (lot_area * 0.12 + np.random.normal(1200, 600, n_samples)).clip(500, 6000)
    full_bath = np.random.randint(1, 5, n_samples)
    half_bath = np.random.randint(0, 3, n_samples)
    garage_cars = np.random.randint(0, 6, n_samples)
    neighborhood = np.random.choice(["UrbanCenter", "SuburbanGreen", "RuralPlain", "LuxuryHeights"], size=n_samples)
    kitchen_qual = np.random.choice(["Fa", "TA", "Gd", "Ex"], size=n_samples)
    
    # Premium Global Features
    smart_home = np.random.choice(["Yes", "No"], p=[0.3, 0.7], size=n_samples)
    basement_area = np.random.uniform(0, 2000, n_samples)
    eco_certified = np.random.choice(["Yes", "No"], p=[0.2, 0.8], size=n_samples)

    # Global Price logic in USD
    price = (gr_liv_area * 180) + (lot_area * 7)
    price += (overall_qual * 30000) + (overall_cond * 6000)
    price += (full_bath * 20000) + (half_bath * 8000) + (garage_cars * 12000)
    price *= np.array([{"UrbanCenter": 1.5, "LuxuryHeights": 2.0, "SuburbanGreen": 1.2, "RuralPlain": 0.75}[n] for n in neighborhood])
    price += (year_built - 1950) * 1200
    price += (basement_area * 50)
    price = np.where(smart_home == "Yes", price + 25000, price)
    price = np.where(eco_certified == "Yes", price + 15000, price)
    
    price += np.random.normal(0, 25000, n_samples)
    price = price.clip(60000, None)

    df = pd.DataFrame({
        "LotArea": lot_area, "OverallQual": overall_qual, "OverallCond": overall_cond,
        "YearBuilt": year_built, "GrLivArea": gr_liv_area, "FullBath": full_bath,
        "HalfBath": half_bath, "GarageCars": garage_cars, "Neighborhood": neighborhood,
        "KitchenQual": kitchen_qual, "SmartHome": smart_home, "BasementArea": basement_area,
        "EcoCertified": eco_certified, "SalePrice": price
    })

    X = df.drop(columns=["SalePrice"])
    y = df["SalePrice"]
    
    NUM = ["LotArea", "OverallQual", "OverallCond", "YearBuilt", "GrLivArea", "FullBath", "HalfBath", "GarageCars", "BasementArea"]
    CAT = ["Neighborhood", "KitchenQual", "SmartHome", "EcoCertified"]
    
    preprocessor = ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), NUM),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("ohe", OneHotEncoder(handle_unknown="ignore"))]), CAT)
    ])
    
    model = Pipeline([("preprocessor", preprocessor), ("xgb", xgb.XGBRegressor(n_estimators=300, max_depth=6, learning_rate=0.04))])
    model.fit(X, y)
    joblib.dump(model, "models/prophet_global.joblib")
    print("Enhanced Global model saved.")

if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    train_india_model()
    train_global_model()
    print("All enhanced models trained successfully!")
