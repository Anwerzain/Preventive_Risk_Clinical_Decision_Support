def get_risk_contributions(patient_data):
    """
    Deterministic explainability layer
    Used in hospitals for transparency
    """

    contributions = {}

    # HbA1c
    if patient_data["HbA1c_level"] >= 6.5:
        contributions["HbA1c"] = 35
    elif patient_data["HbA1c_level"] >= 5.7:
        contributions["HbA1c"] = 20
    else:
        contributions["HbA1c"] = 5

    # BMI
    if patient_data["bmi"] >= 30:
        contributions["BMI"] = 25
    elif patient_data["bmi"] >= 25:
        contributions["BMI"] = 15
    else:
        contributions["BMI"] = 5

    # Glucose
    if patient_data["blood_glucose_level"] >= 200:
        contributions["Blood Glucose"] = 20
    elif patient_data["blood_glucose_level"] >= 140:
        contributions["Blood Glucose"] = 12
    else:
        contributions["Blood Glucose"] = 5

    # Smoking
    if patient_data["smoking_history"] in ["current", "occasional"]:
        contributions["Smoking"] = 10
    else:
        contributions["Smoking"] = 2

    # Hypertension
    if patient_data["hypertension"] == 1:
        contributions["Hypertension"] = 8

    # Heart Disease
    if patient_data["heart_disease"] == 1:
        contributions["Heart Disease"] = 10

    return contributions
