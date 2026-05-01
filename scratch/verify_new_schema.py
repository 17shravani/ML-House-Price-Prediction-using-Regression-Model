import requests
import json

URL = "http://127.0.0.1:8000/predict/india"
data = {
    "BHK": 3,
    "SqftArea": 1500,
    "Bathrooms": 2,
    "Balconies": 2,
    "CityTier": "Tier 1 (Metro)",
    "LocationType": "City Center",
    "Furnishing": "Semi-Furnished",
    "PropertyAge": 5,
    "PowerBackup": "Yes",
    "GatedSecurity": "Yes",
    "ParkingSpaces": 2,
    "MetroDistance": 0.5,
    "Clubhouse": "Yes"
}

try:
    # Note: Backend needs to be running for this to work.
    # This is just a structural test of the data.
    print(f"Testing with payload: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"Error: {e}")
