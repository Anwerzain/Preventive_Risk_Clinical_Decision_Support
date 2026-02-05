def next_steps(risk_category):
    if risk_category == "High":
        return [
            "Order confirmatory laboratory tests (HbA1c, fasting glucose)",
            "Schedule follow-up consultation within 3 months",
            "Provide lifestyle and dietary counselling",
            "Consider referral to specialist if required"
        ]

    elif risk_category == "Moderate":
        return [
            "Advise lifestyle modification",
            "Repeat screening in 6 months",
            "Monitor blood glucose and weight regularly"
        ]

    else:
        return [
            "Continue routine annual screening",
            "Maintain healthy diet and physical activity"
        ]
