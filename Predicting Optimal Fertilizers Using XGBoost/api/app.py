import os
from fastapi import FastAPI
import numpy as np
from sklearn.preprocessing import LabelEncoder
import requests
import pickle

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


app = FastAPI()
le = LabelEncoder()

# path to models folder
base_path = os.path.dirname(os.path.abspath(__file__)) + '\\'
models_path = os.path.join(base_path , '..', 'models')
models_path = os.path.abspath(models_path)

# loading xgb classifier trained model
def load_model():
    with open(models_path+'\\'+ 'model.pkl', 'rb') as f:
        model = pickle.load(f)
        return model

#loading lebel encoder model
def load_label_encoder():
    with open(models_path+'\\'+ 'le_soil.pkl', 'rb') as f_soil:
        le_soil = pickle.load(f_soil)
    with open(models_path+'\\'+ 'le_crop.pkl', 'rb') as f_crop:
        le_crop = pickle.load(f_crop)
    with open(models_path+'\\'+ 'le_fert.pkl', 'rb') as f_fert:
        le_fert = pickle.load(f_fert)
        return le_soil, le_crop, le_fert

load_model()

# endpoint to predict fertilizer name
@app.get('/predict/{Temparature}/{Humidity}/{Moisture}/{Soil}/{Crop}/{Nitrogen}/{Potassium}/{Phosphorous}')
def predict(
    Temparature: float,
    Humidity: float,
    Moisture: float,
    Soil: str,
    Crop: str,
    Nitrogen: int,
    Potassium: int,
    Phosphorous: int
):
    model = load_model()
    le_soil, le_crop, le_fert = load_label_encoder()

    soil = le_soil.transform([Soil])[0]
    crop = le_crop.transform([Crop])[0]

    features = np.array([[Temparature, Humidity, Moisture, soil, crop, Nitrogen, Potassium, Phosphorous]], dtype=float)

    prediction = model.predict(features)
    fertilizer = le_fert.inverse_transform(prediction)[0]

    return {'fertilizer': fertilizer}

#predict()
#load_label_encoder()