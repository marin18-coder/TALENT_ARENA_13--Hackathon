import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

model, feature_order = joblib.load("fraud_model.pkl")


def aggregate_table(rows):
    df = pd.DataFrame(rows)
    features = {}

    for col in df.columns:
        if np.issubdtype(df[col].dtype, np.number):
            features[f"{col}_mean"] = df[col].mean()
            features[f"{col}_sum"] = df[col].sum()
            features[f"{col}_max"] = df[col].max()
            features[f"{col}_min"] = df[col].min()
            features[f"{col}_std"] = df[col].std()

    return features


def build_features(sample):
    features = {}
    features.update(aggregate_table(sample["table_a_last20"]))
    features.update(aggregate_table(sample["table_b_last20"]))
    features.update(aggregate_table(sample["table_c_last20"]))
    features["number_recycled"] = sample["number_recycled"]
    features["kyc_match"] = sample["kyc_match"]
    return features


class FraudRequest(BaseModel):
    table_a_last20: List[Dict[str, Any]]
    table_b_last20: List[Dict[str, Any]]
    table_c_last20: List[Dict[str, Any]]
    number_recycled: int
    kyc_match: int


@app.post("/predict")
def predict(request: FraudRequest):
    features = build_features(request.dict())

    df = pd.DataFrame([features])
    df = df.reindex(columns=feature_order, fill_value=0)

    prob = model.predict_proba(df)[0][1]

    return {
        "risk_score": float(prob)
    }