import streamlit as st

# ----------------------------
# STREAMLIT CONFIG (🔥 MUST BE FIRST)
# ----------------------------
st.set_page_config(
    page_title="Preventive Clinical Decision Support",
    page_icon="🩺",
    layout="wide"
)

# ----------------------------
# GLOBAL STYLES
# ----------------------------
st.markdown("""
<style>
footer {visibility: hidden;}
header {visibility: hidden;}

.main {
    background-color: #f7f9fc;
}

.card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}

.section-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #1f4fd8;
    margin-bottom: 0.5rem;
}

.helper {
    color: #6b7280;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# DB INIT (VERY IMPORTANT)
# ----------------------------
from src.core.db import init_db
init_db()

# ----------------------------
# UI IMPORTS
# ----------------------------
from src.ui.landing import landing_page
from src.ui.patient_form import patient_form
from src.ui.login import login_page
from src.ui.doctor_dashboard import doctor_dashboard

# ----------------------------
# SESSION STATE INIT
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------
with st.sidebar:
    st.markdown("## 🧭 Navigation")

    nav_items = ["Home", "Patient Assessment"]

    if "doctor" in st.session_state:
        nav_items.append("Doctor Dashboard")
    else:
        nav_items.append("Doctor Login")

    selected = st.radio(
        "Go to",
        nav_items,
        index=nav_items.index(st.session_state.page)
        if st.session_state.page in nav_items else 0
    )

    st.session_state.page = selected

    # Logout (only for doctor)
    if "doctor" in st.session_state:
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.session_state.page = "Home"
            st.rerun()

# ----------------------------
# PAGE ROUTING
# ----------------------------
if st.session_state.page == "Home":
    landing_page()

elif st.session_state.page == "Patient Assessment":
    patient_form()

elif st.session_state.page == "Doctor Login":
    login_page()

elif st.session_state.page == "Doctor Dashboard":
    if "doctor" not in st.session_state:
        st.warning("🔒 Please login as doctor first")
        st.session_state.page = "Doctor Login"
        st.rerun()
    else:
        doctor_dashboard()
