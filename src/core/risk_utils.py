# core/risk_utils.py


SUPPORTED_DISEASES = [
    "diabetes",
    "hypertension",
    "heart_disease"
]

def get_features_for_disease(disease: str):
    feature_map = {
        "diabetes": ["age", "bmi", "glucose", "blood_pressure"],
        "hypertension": ["age", "systolic_bp", "diastolic_bp"],
        "heart_disease": ["age", "cholesterol", "smoking"]
    }
    return feature_map.get(disease, [])

def get_risk_ui(risk_level):
    risk_level = str(risk_level).lower()

    if risk_level == "low":
        return {
            "label": "Low Risk",
            "color": "#16a34a",
            "emoji": "🟢",
            "message": "Low diabetes risk. Maintain healthy lifestyle."
        }

    if risk_level == "moderate":
        return {
            "label": "Moderate Risk",
            "color": "#f59e0b",
            "emoji": "🟡",
            "message": "Moderate risk detected. Lifestyle improvement advised."
        }

    if risk_level == "high":
        return {
            "label": "High Risk",
            "color": "#dc2626",
            "emoji": "🔴",
            "message": "High risk detected. Clinical follow-up recommended."
        }

    return {
        "label": "Unknown",
        "color": "#6b7280",
        "emoji": "⚪",
        "message": "Risk level unavailable."
    }
