import joblib
import pandas as pd
import os

model_path = "models/prophet_real_xgb.joblib"
if os.path.exists(model_path):
    try:
        model = joblib.load(model_path)
        print("Model loaded successfully")
        
        # Test prediction
        test_data = pd.DataFrame([{
            "BHK": 3,
            "SqftArea": 1500,
            "Bathrooms": 2,
            "Balconies": 2,
            "CityTier": "Tier 1 (Metro)",
            "LocationType": "City Center",
            "Furnishing": "Semi-Furnished",
            "PropertyAge": 5,
            "PowerBackup": "Yes"
        }])
        pred = model.predict(test_data)
        print(f"Test prediction: {pred[0]}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Model not found")
