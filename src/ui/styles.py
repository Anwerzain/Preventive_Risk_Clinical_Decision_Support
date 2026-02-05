import streamlit as st

def apply_styles():
    st.markdown("""
    <style>

    /* ================= BASE ================= */
    html, body {
        background-color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }

    * {
        transition: all 0.25s ease-in-out;
    }

    /* ================= NAVBAR ================= */
    .navbar {
        background: linear-gradient(90deg, #2563eb, #1e40af);
        padding: 16px 24px;
        border-radius: 14px;
        color: white;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(37,99,235,0.35);
    }

    /* ================= CARDS ================= */
    .card {
        background: white;
        padding: 22px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.06);
        animation: fadeIn 0.4s ease-in;
    }

    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 18px 36px rgba(0,0,0,0.12);
    }

    /* ================= HEADERS ================= */
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* ================= BUTTONS ================= */
    .stButton > button {
        background: linear-gradient(90deg, #2563eb, #1e40af);
        color: white;
        border-radius: 14px;
        padding: 12px 22px;
        font-weight: 600;
        border: none;
        box-shadow: 0 8px 20px rgba(37,99,235,0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 30px rgba(37,99,235,0.55);
    }

    /* ================= RISK COLORS ================= */
    .low { border-left: 6px solid #22c55e; }
    .medium { border-left: 6px solid #f97316; }
    .high { border-left: 6px solid #ef4444; }

    /* ================= ANIMATIONS ================= */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    </style>
    """, unsafe_allow_html=True)
