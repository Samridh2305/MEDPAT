# ml/services/predictor.py

import joblib
import pandas as pd

from common.config import settings

MODEL_DIR = settings.MODEL_DIR

diabetes_model = joblib.load(
    MODEL_DIR / "diabetes_model.pkl"
)

kidney_model = joblib.load(
    MODEL_DIR / "kidney_disease_model.pkl"
)

hypertension_model = joblib.load(
    MODEL_DIR / "hypertension_model.pkl"
)


def predict_diseases(
    features: pd.DataFrame,
) -> dict:

    diabetes_prob = (
        diabetes_model
        .predict_proba(features)[0][1]
    )

    kidney_prob = (
        kidney_model
        .predict_proba(features)[0][1]
    )

    hypertension_prob = (
        hypertension_model
        .predict_proba(features)[0][1]
    )

    return {
        "diabetes_risk": round(
            diabetes_prob * 100,
            1,
        ),
        "kidney_risk": round(
            kidney_prob * 100,
            1,
        ),
        "hypertension_risk": round(
            hypertension_prob * 100,
            1,
        ),
    }