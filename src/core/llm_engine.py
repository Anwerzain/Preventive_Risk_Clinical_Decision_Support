import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_llm_explanation(patient_data, risk, prob, audience="patient"):
    """
    audience: 'patient' | 'clinician'
    """

    prompt = f"""
You are a responsible clinical AI assistant.

Audience: {audience}

Patient data:
{patient_data}

Predicted diabetes risk level: {risk}
Risk probability: {prob:.2f}

Rules:
- Do NOT diagnose
- Explain clearly
- Suggest preventive actions
- Simple language for patients
- Clinical tone for doctors
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text
