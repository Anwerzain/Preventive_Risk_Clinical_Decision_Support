import streamlit as st

def render_layout():
    st.title("🏥 Preventive Diabetes Risk Decision Support")
    st.caption("India-level ML Clinical Decision Support System")

    st.sidebar.header("Patient Inputs")

    with st.sidebar.form(key="patient_form"):
        data = {
            "gender": st.selectbox("Gender", ["Male", "Female"]),
            "age": st.slider("Age", 18, 90, 35),
            "hypertension": st.selectbox("Hypertension", [0, 1]),
            "heart_disease": st.selectbox("Heart Disease", [0, 1]),
            "smoking_history": st.selectbox(
                "Smoking History",
                ["never", "former", "current", "not current", "ever"]
            ),
            "bmi": st.slider("BMI", 10.0, 50.0, 25.0),
            "HbA1c_level": st.slider("HbA1c Level", 4.0, 15.0, 5.6),
            "blood_glucose_level": st.slider("Blood Glucose Level", 70, 300, 120),
        }

        submitted = st.form_submit_button("🔍 Submit for Risk Assessment")

    return submitted, data
