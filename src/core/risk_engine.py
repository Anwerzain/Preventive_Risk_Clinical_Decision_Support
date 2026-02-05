import pickle
import pandas as pd

MODEL_PATH = "train/model.pkl"

with open(MODEL_PATH, "rb") as f:
    model, scaler, feature_names = pickle.load(f)

def compute_risk(patient_data):
    df = pd.DataFrame([patient_data])

    df_encoded = pd.get_dummies(df)
    df_encoded = df_encoded.reindex(columns=feature_names, fill_value=0)

    X_scaled = scaler.transform(df_encoded)
    prob = model.predict_proba(X_scaled)[0][1]

    if prob < 0.3:
        risk = "Low"
    elif prob < 0.6:
        risk = "Moderate"
    else:
        risk = "High"

    return prob, risk, model, feature_names
