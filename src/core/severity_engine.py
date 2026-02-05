def get_severity(risk_probability: float):
    """
    Convert risk probability into
    Severity Level, Urgency, Action & UI color
    """

    risk_pct = risk_probability * 100

    if risk_pct < 20:
        return {
            "level": 0,
            "label": "Normal",
            "urgency": "None",
            "action": "Maintain healthy lifestyle",
            "color": "green"
        }

    elif risk_pct < 40:
        return {
            "level": 1,
            "label": "Mild Risk",
            "urgency": "Low",
            "action": "Lifestyle modification recommended",
            "color": "lime"
        }

    elif risk_pct < 60:
        return {
            "level": 2,
            "label": "Moderate Risk",
            "urgency": "Medium",
            "action": "Regular monitoring & medical advice",
            "color": "orange"
        }

    elif risk_pct < 80:
        return {
            "level": 3,
            "label": "High Risk",
            "urgency": "High",
            "action": "Doctor consultation advised",
            "color": "red"
        }

    else:
        return {
            "level": 4,
            "label": "Critical Risk",
            "urgency": "Critical",
            "action": "Immediate medical attention required",
            "color": "darkred"
        }
