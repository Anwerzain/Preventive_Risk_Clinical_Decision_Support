import streamlit as st
import re
from .styles import apply_styles

from src.core.risk_engine import compute_risk
from src.core.genai_explainer import explain
from src.core.db import get_connection
from src.core.utils import generate_patient_id
from src.core.i18n import get_text

apply_styles()

# =====================================================
# RISK SEVERITY + UI ENGINE (SAFE & LOCAL)
# =====================================================
def get_risk_ui(prob):
    pct = prob * 100

    if pct < 20:
        return {
            "label": "Normal",
            "emoji": "🟢",
            "color": "#22c55e",
            "message": "No immediate diabetes risk. Maintain healthy habits.",
            "urgency": "None"
        }
    elif pct < 40:
        return {
            "label": "Mild Risk",
            "emoji": "🟡",
            "color": "#eab308",
            "message": "Early risk detected. Lifestyle changes recommended.",
            "urgency": "Low"
        }
    elif pct < 60:
        return {
            "label": "Moderate Risk",
            "emoji": "🟠",
            "color": "#f97316",
            "message": "Moderate diabetes risk. Regular monitoring advised.",
            "urgency": "Medium"
        }
    elif pct < 80:
        return {
            "label": "High Risk",
            "emoji": "🔴",
            "color": "#ef4444",
            "message": "High risk detected. Doctor consultation advised.",
            "urgency": "High"
        }
    else:
        return {
            "label": "Critical Risk",
            "emoji": "🚨",
            "color": "#7f1d1d",
            "message": "Critical condition. Immediate medical attention required.",
            "urgency": "Critical"
        }


# =====================================================
# MAIN PATIENT FORM
# =====================================================
def patient_form():

    # -----------------------------
    # STEP STATE
    # -----------------------------
    if "step" not in st.session_state:
        st.session_state.step = "language"

    # =================================================
    # STEP 1: LANGUAGE SELECTION
    # =================================================
    if st.session_state.step == "language":

        st.markdown("""
        <div class="card">
            <div class="section-title">🌐 Select Language / भाषा चुनें</div>
        """, unsafe_allow_html=True)

        language = st.radio("Language / भाषा", ["English", "Hindi"])

        if st.button("Continue / आगे बढ़ें", use_container_width=True):
            st.session_state.language = language
            st.session_state.step = "personal"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Load language text
    T = get_text(st.session_state.language)

    # =================================================
    # STEP 2: PERSONAL DETAILS
    # =================================================
    if st.session_state.step == "personal":

        st.markdown(f"""
        <div class="card">
            <div class="section-title">👤 {T['personal_details']}</div>
        """, unsafe_allow_html=True)

        name = st.text_input(T["full_name"]).strip()
        mobile = st.text_input(T["mobile"]).strip()

        mobile_valid = re.match(r"^[6-9]\d{9}$", mobile)

        if st.button(T["proceed"], use_container_width=True):
            if not name or not mobile_valid:
                st.error(
                    "Please enter valid details"
                    if st.session_state.language == "English"
                    else "कृपया सही जानकारी भरें"
                )
            else:
                st.session_state.name = name
                st.session_state.mobile = mobile
                st.session_state.step = "medical"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        return

    # =================================================
    # STEP 3: MEDICAL FORM
    # =================================================
    if st.session_state.step == "medical":

        # -----------------------------
        # HEADER
        # -----------------------------
        st.markdown(f"""
        <div class="card">
            <div class="section-title">🧍 {T['health_form']}</div>
        """, unsafe_allow_html=True)

        if "patient_id" not in st.session_state:
            st.session_state.patient_id = generate_patient_id()

        st.text_input(
            T["patient_id"],
            value=st.session_state.patient_id,
            disabled=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # BASIC INFO
        # -----------------------------
        st.markdown(f"""
        <div class="card">
            <div class="section-title">🧾 {T['basic_info']}</div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            gender = st.radio(T["gender"], ["Male", "Female"], horizontal=True)
        with col2:
            age = st.slider(T["age"], 18, 90, 35)

        st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # MEDICAL HISTORY
        # -----------------------------
        st.markdown(f"""
        <div class="card">
            <div class="section-title">🩺 {T['medical_history']}</div>
        """, unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            hypertension_ui = st.radio(T["hypertension"], ["No", "Yes"], horizontal=True)
        with col4:
            heart_disease_ui = st.radio(T["heart_disease"], ["No", "Yes"], horizontal=True)

        smoking_ui = st.selectbox(
            T["smoking"],
            ["Never", "Former", "Occasional", "Current"]
            if st.session_state.language == "English"
            else ["कभी नहीं", "पहले करता था", "कभी-कभी", "वर्तमान"]
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # CLINICAL MEASUREMENTS
        # -----------------------------
        st.markdown(f"""
        <div class="card">
            <div class="section-title">🧪 {T['clinical']}</div>
        """, unsafe_allow_html=True)

        bmi = st.slider("BMI", 10.0, 50.0, 25.0)
        hba1c = st.slider("HbA1c (%)", 4.0, 15.0, 5.6)
        glucose = st.slider("Blood Glucose (mg/dL)", 70, 300, 120)

        st.markdown("</div>", unsafe_allow_html=True)

        # =================================================
        # SUBMIT
        # =================================================
        if st.button(T["check_risk"], use_container_width=True):

            patient_data = {
                "gender": gender,
                "age": age,
                "hypertension": 1 if hypertension_ui == "Yes" else 0,
                "heart_disease": 1 if heart_disease_ui == "Yes" else 0,
                "smoking_history": smoking_ui.lower(),
                "bmi": bmi,
                "HbA1c_level": hba1c,
                "blood_glucose_level": glucose
            }

            prob, risk, _, _ = compute_risk(patient_data)
            risk_ui = get_risk_ui(prob)

            # -----------------------------
            # SAVE TO DATABASE
            # -----------------------------
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO patient_records
            (patient_id, name, mobile, language, gender, age,
             hypertension, heart_disease, smoking_history,
             bmi, hba1c, glucose, risk_probability, risk_category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                st.session_state.patient_id,
                st.session_state.name,
                st.session_state.mobile,
                st.session_state.language,
                gender,
                age,
                patient_data["hypertension"],
                patient_data["heart_disease"],
                patient_data["smoking_history"],
                bmi,
                hba1c,
                glucose,
                round(prob, 3),
                risk
            ))
            conn.commit()
            conn.close()

            # -----------------------------
            # RESULT UI
            # -----------------------------
            st.markdown(f"""
            <div class="card" style="border-left:6px solid {risk_ui['color']}">
                <h2>{risk_ui['emoji']} {risk_ui['label']}</h2>
                <p><b>{T['risk_result']}:</b> {prob*100:.2f}%</p>
                <p><b>Urgency:</b> {risk_ui['urgency']}</p>
                <p>{risk_ui['message']}</p>
            </div>
            """, unsafe_allow_html=True)

            # -----------------------------
            # AI EXPLANATION (SAFE FALLBACK)
            # -----------------------------
            st.markdown(f"""
            <div class="card">
                <div class="section-title">🤖 {T['ai_explanation']}</div>
            """, unsafe_allow_html=True)

            try:
                st.write(
                    explain(
                        patient_data=patient_data,
                        risk=risk,
                        prob=prob,
                        audience="patient"
                    )
                )
            except Exception:
                st.info(
                    "AI explanation temporarily unavailable. Please consult a doctor."
                    if st.session_state.language == "English"
                    else "AI जानकारी उपलब्ध नहीं है। कृपया डॉक्टर से सलाह लें।"
                )

            st.markdown("</div>", unsafe_allow_html=True)

            # -----------------------------
            # RESET SESSION
            # -----------------------------
            for key in ["step", "patient_id", "name", "mobile", "language"]:
                if key in st.session_state:
                    del st.session_state[key]
