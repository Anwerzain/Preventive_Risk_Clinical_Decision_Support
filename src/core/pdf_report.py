from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

def generate_pdf(patient_record: dict, explanation: str):
    os.makedirs("reports", exist_ok=True)

    patient_id = patient_record["patient_id"]
    language = patient_record.get("language", "English")

    file_path = f"reports/{patient_id}_report.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # -----------------------------
    # LANGUAGE TEXT
    # -----------------------------
    if language == "Hindi":
        title = "डायबिटीज़ जोखिम मूल्यांकन रिपोर्ट"
        subtitle = "AI आधारित निवारक स्वास्थ्य रिपोर्ट"
        patient_label = "रोगी विवरण"
        clinical_label = "क्लिनिकल माप"
        risk_label = "जोखिम परिणाम"
        ai_label = "AI व्याख्या"
        disclaimer = (
            "⚠️ यह रिपोर्ट केवल सूचना हेतु है। "
            "यह किसी भी प्रकार का चिकित्सीय निदान नहीं है।"
        )
    else:
        title = "Diabetes Risk Assessment Report"
        subtitle = "AI-based Preventive Health Report"
        patient_label = "Patient Details"
        clinical_label = "Clinical Measurements"
        risk_label = "Risk Outcome"
        ai_label = "AI Explanation"
        disclaimer = (
            "⚠️ This report is for informational purposes only. "
            "It does not constitute a medical diagnosis."
        )

    # -----------------------------
    # HEADER
    # -----------------------------
    story.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(subtitle, styles["Italic"]))
    story.append(Spacer(1, 12))

    # -----------------------------
    # PATIENT DETAILS
    # -----------------------------
    story.append(Paragraph(f"<b>{patient_label}</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph(f"Patient ID: {patient_id}", styles["Normal"]))
    story.append(Paragraph(f"Gender: {patient_record['gender']}", styles["Normal"]))
    story.append(Paragraph(f"Age: {patient_record['age']}", styles["Normal"]))
    story.append(Spacer(1, 10))

    # -----------------------------
    # CLINICAL DATA
    # -----------------------------
    story.append(Paragraph(f"<b>{clinical_label}</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph(f"BMI: {patient_record['bmi']}", styles["Normal"]))
    story.append(Paragraph(f"HbA1c: {patient_record['hba1c']} %", styles["Normal"]))
    story.append(Paragraph(
        f"Blood Glucose: {patient_record['glucose']} mg/dL",
        styles["Normal"]
    ))
    story.append(Spacer(1, 10))

    # -----------------------------
    # RISK RESULT
    # -----------------------------
    story.append(Paragraph(f"<b>{risk_label}</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        f"Risk Probability: {patient_record['risk_probability']*100:.2f} %",
        styles["Normal"]
    ))
    story.append(Paragraph(
        f"Risk Category: {patient_record['risk_category']}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 10))

    # -----------------------------
    # AI EXPLANATION
    # -----------------------------
    story.append(Paragraph(f"<b>{ai_label}</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(explanation, styles["Normal"]))
    story.append(Spacer(1, 14))

    # -----------------------------
    # DISCLAIMER
    # -----------------------------
    story.append(Paragraph(disclaimer, styles["Italic"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        styles["Normal"]
    ))

    doc.build(story)
    return file_path
