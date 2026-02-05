from src.core.llm_engine import generate_llm_explanation


def _rule_based_summary(patient_data):
    """
    Deterministic medical reasoning (safe + explainable)
    """
    insights = []

    if patient_data["HbA1c_level"] >= 6.5:
        insights.append(
            "HbA1c level is elevated, suggesting poor long-term glucose control."
        )

    if patient_data["blood_glucose_level"] >= 140:
        insights.append(
            "Blood glucose level is above normal range."
        )

    if patient_data["bmi"] >= 30:
        insights.append(
            "BMI indicates obesity, increasing insulin resistance risk."
        )

    if patient_data["hypertension"] == 1:
        insights.append(
            "Hypertension present, increasing cardiovascular risk."
        )

    if patient_data["heart_disease"] == 1:
        insights.append(
            "Existing heart disease increases risk of diabetes-related complications."
        )

    if patient_data["smoking_history"] in ["current", "occasional"]:
        insights.append(
            "Smoking history contributes to metabolic and vascular risk."
        )

    if not insights:
        insights.append(
            "No major clinical risk drivers detected from the provided data."
        )

    return insights


def explain(patient_data, risk, prob, audience="patient"):
    """
    Hybrid explanation engine:
    - Rule-based medical reasoning (always available)
    - GenAI explanation (optional, fail-safe)
    """

    rule_insights = _rule_based_summary(patient_data)

    # -----------------------------
    # TRY GENAI (OPTIONAL LAYER)
    # -----------------------------
    try:
        ai_text = generate_llm_explanation(
            patient_data=patient_data,
            risk=risk,
            prob=prob,
            audience=audience
        )
        return ai_text

    # -----------------------------
    # FAIL-SAFE FALLBACK (IMPORTANT)
    # -----------------------------
    except Exception:
        if audience == "clinician":
            return (
                f"Predicted {risk} diabetes risk "
                f"({prob*100:.2f}%). "
                f"Key contributing factors include: "
                f"{'; '.join(rule_insights)}. "
                "This assessment should be used as a screening aid. "
                "Recommend lifestyle modification, metabolic monitoring, "
                "and appropriate follow-up testing."
            )
        else:
            return (
                f"Based on your health details, your diabetes risk is {risk.lower()} "
                f"({prob*100:.2f}%). "
                "Some factors affecting this risk include diet, weight, "
                "and blood sugar levels. "
                "Healthy eating, daily walking, and regular check-ups "
                "can help reduce future risk."
            )
