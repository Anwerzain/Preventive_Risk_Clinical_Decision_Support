"""
Human-facing explanation layer
Used to communicate ML risk outputs clearly to:
1. Clinicians (OPD / hospital workflow)
2. Patients (non-technical, reassuring language)

This file does NOT make predictions.
It only explains them.
"""


def top_risk_factors(model, features, k=5):
    """
    ML-centric explanation (for judges / audit / debugging)
    Returns top-k influential features from linear models
    """
    coef = model.coef_[0]
    ranked = sorted(
        zip(features, coef),
        key=lambda x: abs(x[1]),
        reverse=True
    )
    return ranked[:k]


# ---------------- CLINICIAN EXPLANATION ---------------- #

def clinician_explanation(risk_category, key_factors=None):
    """
    Professional explanation for doctors
    OPD-grade, neutral, non-alarming
    """

    explanation = (
        f"Predicted diabetes risk category: {risk_category}. "
        "This assessment is generated using a combination of "
        "machine learning models and validated clinical rules.\n\n"
    )

    if key_factors:
        explanation += "Key contributing clinical factors identified:\n"
        for factor in key_factors:
            explanation += f"- {factor}\n"

        explanation += "\n"

    explanation += (
        "This output is intended for early screening and decision support only. "
        "Final diagnosis and treatment decisions should be made by a qualified clinician "
        "based on full clinical evaluation."
    )

    return explanation


# ---------------- PATIENT EXPLANATION ---------------- #

def patient_explanation(risk_category):
    """
    Patient-friendly explanation
    Simple language, reassuring tone
    No percentages, no medical jargon
    """

    if risk_category == "High":
        risk_text = "higher than normal"
    elif risk_category == "Moderate":
        risk_text = "moderate"
    else:
        risk_text = "low"

    return (
        f"Based on the information you provided, your current risk of developing diabetes "
        f"appears to be **{risk_text}**.\n\n"
        "This does NOT mean that you have diabetes right now.\n\n"
        "It only helps identify whether extra care, healthier habits, or regular checkups "
        "may help prevent problems in the future.\n\n"
        "Maintaining a healthy lifestyle, balanced diet, physical activity, and periodic "
        "health monitoring can significantly reduce future risk."
    )


# ---------------- COUNTERFACTUAL GUIDANCE ---------------- #

def counterfactuals(patient_data):
    """
    Actionable prevention tips
    Used in What-If simulation
    """

    tips = []

    if patient_data.get("HbA1c_level", 0) > 6.5:
        tips.append("Lowering HbA1c through diet, exercise, or medication can reduce risk.")

    if patient_data.get("bmi", 0) > 27:
        tips.append("Reducing body weight by 5–7% can significantly lower diabetes risk.")

    if patient_data.get("smoking_history") in ["current", "ever"]:
        tips.append("Quitting smoking is strongly recommended for long-term health.")

    if not tips:
        tips.append("Continue your current healthy lifestyle and routine health checkups.")

    return tips
