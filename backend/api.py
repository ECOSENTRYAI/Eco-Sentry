import os

import ee
import google.generativeai as genai
import pandas as pd
import joblib
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.oauth2 import service_account

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Earth Engine Service Account Authentication
try:
    SERVICE_ACCOUNT = 'wildfire-ee-service@ee-titasghosh7.iam.gserviceaccount.com'
    CREDENTIALS = service_account.Credentials.from_service_account_file(
        'EE_KEY_JSON',
        scopes=['https://www.googleapis.com/auth/earthengine']
    )
    ee.Initialize(credentials=CREDENTIALS)
    logging.info("Earth Engine initialized successfully")
except Exception as e:
    logging.error(f"Earth Engine initialization failed: {e}")
    raise RuntimeError("Failed to initialize Earth Engine") from e

# Initialize Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel('gemini-2.0-flash')

class WildfirePredictor:
    def __init__(self):
        try:
            self.model = joblib.load("wildfire_model.joblib")
            logging.info("Model loaded successfully")
        except Exception as e:
            logging.error(f"Model loading failed: {e}")
            raise

    def _get_geo_features(self, lat: float, lon: float):
        """Get Earth Engine features with error handling"""
        try:
            point = ee.Geometry.Point(lon, lat)
            elevation_img = ee.Image('USGS/SRTMGL1_003')
            elevation = elevation_img.sample(point, 30).first().get('elevation').getInfo()
            return {
                'ndvi': 0.5,  # Add actual EE calculations if needed
                'lst': 300,
                'elevation': elevation if elevation else 500,
                'landcover_type': 1,
                'climate_zone': 1,
                'precip': 0
            }
        except Exception as e:
            logging.error(f"Earth Engine error: {e}")
            return {
                'ndvi': 0.5,
                'lst': 300,
                'elevation': 500,
                'landcover_type': 1,
                'climate_zone': 1,
                'precip': 0
            }

    def predict(self, lat: float, lon: float):
        """Safe prediction with error handling"""
        try:
            features = self._get_geo_features(lat, lon)
            df = pd.DataFrame([features])
            return float(self.model.predict_proba(df)[0][1])
        except Exception as e:
            logging.error(f"Prediction error: {e}")
            return 0.5  # Fallback value

# Initialize FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = WildfirePredictor()

class LocationRequest(BaseModel):
    location: str

def get_coordinates(location: str):
    """Convert location text to coordinates using Gemini"""
    try:
        response = gemini.generate_content(
            f"Convert this location to decimal latitude,longitude: {location}. "
            "Return ONLY numbers separated by comma, nothing else."
        )
        if not response.text:
            raise ValueError("Empty response from Gemini")
        return map(float, response.text.strip().split(','))
    except Exception as e:
        logging.error(f"Location conversion error: {e}")
        raise

@app.post("/predict")
async def predict_risk(request: LocationRequest):
    try:
        lat, lon = get_coordinates(request.location)
        risk_percent = predictor.predict(lat, lon) * 100
        return {
            "risk": round(risk_percent, 2),
            "coordinates": {"lat": lat, "lon": lon},
            "location": request.location
        }
    except Exception as e:
        logging.error(f"API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
