import streamlit as st
from auth import authenticate

def login_page():
    st.title("👨‍⚕️ Doctor Login")
    st.caption("Authorized access only")

    # Already logged in → redirect
    if "doctor" in st.session_state:
        st.session_state["page"] = "Doctor Dashboard"
        st.rerun()

    username = st.text_input("Username", placeholder="doctor1")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username.strip(), password.strip()):
            st.session_state["doctor"] = username.strip()
            st.session_state["page"] = "Doctor Dashboard"
            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")
