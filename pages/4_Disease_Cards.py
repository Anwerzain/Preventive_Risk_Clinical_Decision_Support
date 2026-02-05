import streamlit as st
from src.core.risk_utils import SUPPORTED_DISEASES, get_features_for_disease

st.set_page_config(
    page_title="Disease Screening Cards",
    layout="wide"
)

st.title("🩺 Multi-Disease Preventive Screening")
st.caption("OPD-grade early risk screening • Click a disease to begin")

st.divider()

# ---------------- SESSION STATE ----------------
if "selected_disease" not in st.session_state:
    st.session_state.selected_disease = None

# ---------------- DISEASE CARDS ----------------
st.subheader("📋 Select Disease")

cols = st.columns(4)

diseases = [
    ("diabetes", "🟦 Diabetes", "Blood sugar & metabolic risk"),
    ("hypertension", "🟥 Blood Pressure", "Cardiovascular risk"),
    ("thyroid", "🟪 Thyroid", "Hormonal imbalance"),
    ("kidney", "🟫 Kidney", "Renal function risk"),
]

for col, disease in zip(cols, diseases):
    key, title, desc = disease
    with col:
        st.markdown(
            f"""
            <div style="
                border:1px solid #ddd;
                border-radius:12px;
                padding:20px;
                text-align:center;
                background-color:#fafafa;
                ">
                <h3>{title}</h3>
                <p style="font-size:14px;">{desc}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(f"Screen {title}", key=key):
            st.session_state.selected_disease = key

st.divider()

# ---------------- DYNAMIC FORM ----------------
if st.session_state.selected_disease:

    disease = st.session_state.selected_disease
    st.subheader(f"🧾 {disease.capitalize()} Screening Form")

    features = get_features_for_disease(disease)

    input_data = {}

    cols = st.columns(3)

    for i, feature in enumerate(features):
        with cols[i % 3]:
            if feature in ["gender", "smoking_history"]:
                options = ["Male", "Female"] if feature == "gender" else ["never", "former", "current"]
                input_data[feature] = st.selectbox(feature.replace("_", " ").title(), options)

            elif feature in ["hypertension", "heart_disease"]:
                input_data[feature] = st.selectbox(
                    feature.replace("_", " ").title(),
                    [0, 1],
                    format_func=lambda x: "Yes" if x == 1 else "No"
                )

            else:
                input_data[feature] = st.number_input(
                    feature.replace("_", " ").title(),
                    min_value=0.0
                )

    st.info("Prediction & explanation will appear in next phase")

else:
    st.info("⬆️ Select a disease card to start screening")
