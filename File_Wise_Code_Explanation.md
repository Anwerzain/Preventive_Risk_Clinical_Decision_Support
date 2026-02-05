# 📄 File-by-File Code Explanation

## Complete Code Analysis with Line-by-Line Breakdown

---

## 📂 CORE FILES

### 1️⃣ app.py - Main Application Entry Point

**Lines 1-35: Global Styles**
```python
import streamlit as st

st.markdown("""
<style>
footer {visibility: hidden;}
header {visibility: hidden;}
...
</style>
""", unsafe_allow_html=True)
```
**Kya kar raha hai**: 
- Streamlit import kar raha hai
- CSS styles inject kar raha hai
- Footer aur header hide kar raha hai
- Custom card designs aur colors apply kar raha hai

**Kyu use ho raha hai**: Professional UI ke liye consistent styling chahiye

---

**Lines 40-43: Streamlit Configuration**
```python
st.set_page_config(
    page_title="Preventive Clinical Decision Support",
    layout="wide"
)
```
**Kya kar raha hai**: Browser tab title aur layout set kar raha hai
**Kyu use ho raha hai**: Wide layout se dashboard better dikhta hai

---

**Lines 48-49: Database Initialization**
```python
from core.db import init_db
init_db()
```
**Kya kar raha hai**: Database aur tables create kar raha hai if not exist
**Kyu use ho raha hai**: App start hote hi database ready hona chahiye

---

**Lines 54-57: UI Imports**
```python
from ui.landing import landing_page
from ui.patient_form import patient_form
from ui.login import login_page
from ui.doctor_dashboard import doctor_dashboard
```
**Kya kar raha hai**: Sab UI components import kar raha hai
**Kyu use ho raha hai**: Modular code organization ke liye

---

**Lines 62-63: Session State Initialization**
```python
if "page" not in st.session_state:
    st.session_state.page = "Home"
```
**Kya kar raha hai**: Default page set kar raha hai
**Kyu use ho raha hai**: User ka current page track karna hai

---

**Lines 68-92: Sidebar Navigation**
```python
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    nav_items = ["Home", "Patient Assessment"]
    
    if "doctor" in st.session_state:
        nav_items.append("Doctor Dashboard")
    else:
        nav_items.append("Doctor Login")
    
    selected = st.radio(...)
    st.session_state.page = selected
    
    if "doctor" in st.session_state:
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()
```
**Kya kar raha hai**: 
- Sidebar mein navigation menu dikha raha hai
- Doctor logged in hai to dashboard dikha raha hai
- Logout button dikha raha hai

**Kyu use ho raha hai**: Easy navigation ke liye

---

**Lines 97-112: Page Routing**
```python
if st.session_state.page == "Home":
    landing_page()
elif st.session_state.page == "Patient Assessment":
    patient_form()
elif st.session_state.page == "Doctor Login":
    login_page()
elif st.session_state.page == "Doctor Dashboard":
    if "doctor" not in st.session_state:
        st.warning("🔒 Please login as doctor first")
        st.rerun()
    else:
        doctor_dashboard()
```
**Kya kar raha hai**: Selected page ke according function call kar raha hai
**Kyu use ho raha hai**: Single page app mein routing ke liye

---

### 2️⃣ core/db.py - Database Operations

**Lines 1-5: Imports & Config**
```python
import sqlite3
import os

DB_PATH = "data/clinical.db"
```
**Kya kar raha hai**: SQLite import aur database path define kar raha hai
**Kyu use ho raha hai**: Database operations ke liye

---

**Lines 8-10: Database Connection**
```python
def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)
```
**Kya kar raha hai**: 
- `data` folder create kar raha hai if not exists
- SQLite connection return kar raha hai
- `check_same_thread=False` se multiple threads access kar sakte hain

**Kyu use ho raha hai**: 
- Database connection centralized ho
- Streamlit multiple threads use karta hai

---

**Lines 13-43: Database Initialization**
```python
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS patient_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        name TEXT,
        mobile TEXT,
        language TEXT,
        gender TEXT,
        age INTEGER,
        hypertension INTEGER,
        heart_disease INTEGER,
        smoking_history TEXT,
        bmi REAL,
        hba1c REAL,
        glucose REAL,
        risk_probability REAL,
        risk_category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()
```
**Kya kar raha hai**: Patient records table create kar raha hai
**Kyu use ho raha hai**: Patient data store karna hai

**Column Details**:
- `id`: Auto-incrementing primary key
- `patient_id`: Unique patient identifier
- `name, mobile, language`: Personal info
- `gender, age`: Demographics
- `hypertension, heart_disease`: Binary flags (0/1)
- `smoking_history`: Text field
- `bmi, hba1c, glucose`: Float values
- `risk_probability`: 0-1 float
- `risk_category`: Low/Moderate/High
- `created_at`: Auto timestamp

---

### 3️⃣ core/risk_engine.py - ML Risk Prediction

**Lines 1-7: Model Loading**
```python
import pickle
import pandas as pd

MODEL_PATH = "train/model.pkl"

with open(MODEL_PATH, "rb") as f:
    model, scaler, feature_names = pickle.load(f)
```
**Kya kar raha hai**: 
- Pickle se trained model, scaler, aur feature names load kar raha hai
- File open hote hi load ho jata hai (module level)

**Kyu use ho raha hai**: 
- Model ek baar load ho, baar-baar nahi
- Fast predictions ke liye

---

**Lines 9-25: Risk Computation**
```python
def compute_risk(patient_data):
    # Step 1: Convert to DataFrame
    df = pd.DataFrame([patient_data])
    
    # Step 2: One-hot encoding
    df_encoded = pd.get_dummies(df)
    
    # Step 3: Align features with training
    df_encoded = df_encoded.reindex(columns=feature_names, fill_value=0)
    
    # Step 4: Scale features
    X_scaled = scaler.transform(df_encoded)
    
    # Step 5: Predict probability
    prob = model.predict_proba(X_scaled)[0][1]
    
    # Step 6: Categorize risk
    if prob < 0.3:
        risk = "Low"
    elif prob < 0.6:
        risk = "Moderate"
    else:
        risk = "High"
    
    return prob, risk, model, feature_names
```

**Step-by-Step Explanation**:

**Step 1**: `df = pd.DataFrame([patient_data])`
- Dictionary ko DataFrame mein convert kar raha hai
- Example: `{"age": 35, "gender": "Male"}` → DataFrame with 1 row

**Step 2**: `df_encoded = pd.get_dummies(df)`
- Categorical variables ko binary columns mein convert kar raha hai
- Example: `gender: Male` → `gender_Male: 1, gender_Female: 0`

**Step 3**: `df_encoded.reindex(columns=feature_names, fill_value=0)`
- Training ke features ke according columns arrange kar raha hai
- Missing columns ko 0 se fill kar raha hai
- **Critical**: Training aur prediction mein same feature order chahiye

**Step 4**: `X_scaled = scaler.transform(df_encoded)`
- StandardScaler se normalize kar raha hai
- Values ko mean=0, std=1 range mein le aata hai
- **Why**: Model training time bhi yahi scaling hui thi

**Step 5**: `prob = model.predict_proba(X_scaled)[0][1]`
- Logistic Regression model se probability predict kar raha hai
- `[0][1]` means: first row, second class (diabetes=1)
- Returns value between 0 and 1

**Step 6**: Risk categorization based on thresholds
- < 30%: Low risk
- 30-60%: Moderate risk
- > 60%: High risk

**Return Values**:
- `prob`: Risk probability (0-1)
- `risk`: Risk category string
- `model`: Model object (for explainability)
- `feature_names`: Feature list (for explainability)

---

### 4️⃣ core/genai_explainer.py - AI Explanation Engine

**Lines 1-45: Rule-based Medical Logic**
```python
def _rule_based_summary(patient_data):
    """
    Deterministic medical reasoning (safe + explainable)
    """
    insights = []
    
    if patient_data["HbA1c_level"] >= 6.5:
        insights.append(
            "HbA1c level is elevated, suggesting poor long-term glucose control."
        )
    
    if patient_data["blood_glucose_level"] >= 140:
        insights.append(
            "Blood glucose level is above normal range."
        )
    
    if patient_data["bmi"] >= 30:
        insights.append(
            "BMI indicates obesity, increasing insulin resistance risk."
        )
    
    # ... more rules
    
    if not insights:
        insights.append(
            "No major clinical risk drivers detected."
        )
    
    return insights
```

**Kya kar raha hai**: 
- Medical thresholds check kar raha hai
- Clinical insights generate kar raha hai
- Deterministic logic use kar raha hai

**Medical Thresholds Used**:
- HbA1c >= 6.5%: Prediabetic range
- Glucose >= 140 mg/dL: Above fasting normal
- BMI >= 30: Obesity
- Hypertension = 1: High BP present
- Heart disease = 1: CVD history
- Smoking: Current/Occasional

**Kyu use ho raha hai**: 
- AI fail hone par bhi explanation mil sake
- Medical guidelines follow karta hai
- Always reliable

---

**Lines 48-91: Hybrid Explanation System**
```python
def explain(patient_data, risk, prob, audience="patient"):
    """
    Hybrid explanation engine:
    - Rule-based medical reasoning (always available)
    - GenAI explanation (optional, fail-safe)
    """
    
    rule_insights = _rule_based_summary(patient_data)
    
    # TRY GENAI (OPTIONAL LAYER)
    try:
        ai_text = generate_llm_explanation(
            patient_data=patient_data,
            risk=risk,
            prob=prob,
            audience=audience
        )
        return ai_text
    
    # FAIL-SAFE FALLBACK (IMPORTANT)
    except Exception:
        if audience == "clinician":
            return (
                f"Predicted {risk} diabetes risk "
                f"({prob*100:.2f}%). "
                f"Key contributing factors include: "
                f"{'; '.join(rule_insights)}. "
                "This assessment should be used as a screening aid..."
            )
        else:
            return (
                f"Based on your health details, your diabetes risk is {risk.lower()} "
                f"({prob*100:.2f}%). "
                "Some factors affecting this risk include diet, weight..."
            )
```

**Kya kar raha hai**:
1. Rule-based insights generate karta hai
2. GenAI se better explanation lene ki koshish karta hai
3. API fail hone par rule-based explanation use karta hai
4. Audience ke according language adjust karta hai

**Two Audiences**:
- **Patient**: Simple, layman language
- **Clinician**: Medical terminology, clinical tone

**Kyu dual approach**:
- **Reliability**: Hamesha kaam kare
- **Quality**: GenAI better explanations deta hai
- **Graceful degradation**: API down hone par bhi system chalte rahe

---

### 5️⃣ core/llm_engine.py - Google Gemini Integration

**Lines 1-14: Setup & Authentication**
```python
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=GEMINI_API_KEY)
```

**Kya kar raha hai**:
- `.env` file se API key load kar raha hai
- Google Gemini client create kar raha hai
- API key validation kar raha hai

**Kyu .env file**:
- API keys code mein nahi hone chahiye (security)
- `.gitignore` mein .env add karke secret safe rahega

---

**Lines 16-45: LLM Explanation Generation**
```python
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
```

**Kya kar raha hai**:
- Medical context ke saath prompt banata hai
- Gemini AI ko call karta hai
- Natural language explanation generate karta hai

**Prompt Structure**:
1. **Role definition**: Clinical AI assistant
2. **Audience context**: Patient ya Clinician
3. **Patient data**: All health parameters
4. **Risk results**: Category aur probability
5. **Safety rules**: 
   - No diagnosis
   - Clear explanations
   - Preventive focus
   - Audience-appropriate language

**Why Gemini-1.5-flash**:
- Fast response
- Good for short explanations
- Cost-effective
- Reliable

---

### 6️⃣ core/pdf_report.py - PDF Report Generator

**Lines 1-6: Imports**
```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os
```

**Libraries**:
- `reportlab`: PDF creation
- `datetime`: Timestamp
- `os`: File operations

---

**Lines 7-13: Function Setup**
```python
def generate_pdf(patient_record: dict, explanation: str):
    os.makedirs("reports", exist_ok=True)
    
    patient_id = patient_record["patient_id"]
    language = patient_record.get("language", "English")
    
    file_path = f"reports/{patient_id}_report.pdf"
```

**Kya kar raha hai**:
- `reports` folder create kar raha hai
- Patient ID aur language extract kar raha hai
- Output file path define kar raha hai

---

**Lines 15-17: PDF Document Setup**
```python
doc = SimpleDocTemplate(file_path, pagesize=A4)
styles = getSampleStyleSheet()
story = []
```

**Kya kar raha hai**:
- A4 size PDF document template create kar raha hai
- Default styles load kar raha hai
- `story` list (content container) initialize kar raha hai

**ReportLab Concept**:
- `story`: List of flowable elements (paragraphs, spacers, tables)
- Elements ko sequentially add karte hain
- End mein `doc.build(story)` se PDF generate hota hai

---

**Lines 20-43: Multi-language Text**
```python
if language == "Hindi":
    title = "डायबिटीज़ जोखिम मूल्यांकन रिपोर्ट"
    subtitle = "AI आधारित निवारक स्वास्थ्य रिपोर्ट"
    patient_label = "रोगी विवरण"
    clinical_label = "क्लिनिकल माप"
    risk_label = "जोखिम परिणाम"
    ai_label = "AI व्याख्या"
    disclaimer = "⚠️ यह रिपोर्ट केवल सूचना हेतु है..."
else:
    title = "Diabetes Risk Assessment Report"
    subtitle = "AI-based Preventive Health Report"
    patient_label = "Patient Details"
    # ... English labels
```

**Kya kar raha hai**: Language ke according labels set kar raha hai
**Kyu**: Report user ki language mein hona chahiye

---

**Lines 46-51: Header Section**
```python
story.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
story.append(Spacer(1, 8))
story.append(Paragraph(subtitle, styles["Italic"]))
story.append(Spacer(1, 12))
```

**Kya kar raha hai**:
- Bold title add kar raha hai
- 8 points spacing
- Italic subtitle
- 12 points spacing

**Spacer(width, height)**: Vertical space add karta hai

---

**Lines 54-62: Patient Details Section**
```python
story.append(Paragraph(f"<b>{patient_label}</b>", styles["Heading2"]))
story.append(Spacer(1, 6))

story.append(Paragraph(f"Patient ID: {patient_id}", styles["Normal"]))
story.append(Paragraph(f"Gender: {patient_record['gender']}", styles["Normal"]))
story.append(Paragraph(f"Age: {patient_record['age']}", styles["Normal"]))
story.append(Spacer(1, 10))
```

**Kya kar raha hai**: Patient ki basic details add kar raha hai

---

**Lines 65-76: Clinical Measurements**
```python
story.append(Paragraph(f"<b>{clinical_label}</b>", styles["Heading2"]))
story.append(Paragraph(f"BMI: {patient_record['bmi']}", styles["Normal"]))
story.append(Paragraph(f"HbA1c: {patient_record['hba1c']} %", styles["Normal"]))
story.append(Paragraph(
    f"Blood Glucose: {patient_record['glucose']} mg/dL",
    styles["Normal"]
))
```

**Kya kar raha hai**: Clinical measurements display kar raha hai

---

**Lines 79-92: Risk Results**
```python
story.append(Paragraph(f"<b>{risk_label}</b>", styles["Heading2"]))
story.append(Paragraph(
    f"Risk Probability: {patient_record['risk_probability']*100:.2f} %",
    styles["Normal"]
))
story.append(Paragraph(
    f"Risk Category: {patient_record['risk_category']}",
    styles["Normal"]
))
```

**Kya kar raha hai**: 
- Risk probability percentage mein display kar raha hai
- Risk category show kar raha hai

**Format**: `{value*100:.2f}` means: 
- `*100`: Convert 0.45 → 45
- `.2f`: Two decimal places → 45.32%

---

**Lines 95-100: AI Explanation**
```python
story.append(Paragraph(f"<b>{ai_label}</b>", styles["Heading2"]))
story.append(Spacer(1, 6))
story.append(Paragraph(explanation, styles["Normal"]))
story.append(Spacer(1, 14))
```

**Kya kar raha hai**: GenAI/Rule-based explanation add kar raha hai

---

**Lines 103-113: Footer (Disclaimer + Timestamp)**
```python
story.append(Paragraph(disclaimer, styles["Italic"]))
story.append(Spacer(1, 10))
story.append(Paragraph(
    f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
    styles["Normal"]
))

doc.build(story)
return file_path
```

**Kya kar raha hai**:
- Medical disclaimer add kar raha hai
- Generation timestamp add kar raha hai
- PDF build kar raha hai
- File path return kar raha hai

**Timestamp Format**: `04-02-2026 15:30`

---

### 7️⃣ core/i18n.py - Internationalization

```python
def get_text(lang):
    TEXT = {
        "English": {
            "select_language": "Select Language",
            "continue": "Continue",
            "personal_details": "Personal Details",
            # ... 30+ labels
        },
        
        "Hindi": {
            "select_language": "भाषा चुनें",
            "continue": "आगे बढ़ें",
            "personal_details": "व्यक्तिगत जानकारी",
            # ... 30+ labels in Hindi
        }
    }
    
    return TEXT[lang]
```

**Kya kar raha hai**: 
- Language-specific text dictionary return karta hai
- Dictionary lookup se O(1) access

**Usage Example**:
```python
T = get_text("Hindi")
print(T["personal_details"])  # Output: "व्यक्तिगत जानकारी"
```

**Why separate file**:
- Centralized translations
- Easy to add new languages
- Clean code separation

---

### 8️⃣ core/decision_support.py - Clinical Recommendations

```python
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
    
    else:  # Low risk
        return [
            "Continue routine annual screening",
            "Maintain healthy diet and physical activity"
        ]
```

**Kya kar raha hai**: 
- Risk category ke according clinical action items return karta hai
- Evidence-based guidelines follow karta hai

**High Risk Actions**:
1. Confirmatory tests order karna
2. 3-month follow-up
3. Lifestyle counseling
4. Specialist referral consider karna

**Moderate Risk Actions**:
1. Lifestyle changes recommend karna
2. 6-month re-screening
3. Regular monitoring

**Low Risk Actions**:
1. Annual screening continue
2. Healthy lifestyle maintain

**Why this function**:
- Standardized clinical workflows
- Doctor ko structured guidance
- Consistent recommendations

---

### 9️⃣ core/utils.py - Utility Functions

```python
from datetime import datetime

def generate_patient_id():
    """
    Generate unique patient ID
    Format: PID-YYYYMMDD-XXXX
    """
    timestamp = datetime.now().strftime("%Y%m%d")
    random_suffix = str(hash(datetime.now()))[-4:]
    return f"PID-{timestamp}-{random_suffix}"
```

**Kya kar raha hai**: Unique patient ID generate karta hai

**Format**: `PID-20260204-8347`
- `PID`: Prefix (Patient ID)
- `20260204`: Date (YYYYMMDD)
- `8347`: Random 4-digit number

**Why this format**:
- Human-readable
- Date sortable
- Unique per patient
- Short enough to type

---

## 📂 UI FILES

### 🔟 ui/patient_form.py - Patient Assessment Form

**Lines 1-11: Imports & Setup**
```python
import streamlit as st
import re
from ui.styles import apply_styles
from core.risk_engine import compute_risk
from core.genai_explainer import explain
from core.db import get_connection
from core.utils import generate_patient_id
from core.i18n import get_text

apply_styles()
```

**Kya kar raha hai**: Required modules import aur styles apply kar raha hai

---

**Lines 16-58: Risk UI Function**
```python
def get_risk_ui(prob):
    pct = prob * 100
    
    if pct < 20:
        return {
            "label": "Normal",
            "emoji": "🟢",
            "color": "#22c55e",
            "message": "No immediate diabetes risk...",
            "urgency": "None"
        }
    elif pct < 40:
        return {
            "label": "Mild Risk",
            "emoji": "🟡",
            "color": "#eab308",
            # ...
        }
    # ... more categories
```

**Kya kar raha hai**: 
- Probability percentage mein convert karta hai
- 5 risk levels define karta hai
- Har level ke liye emoji, color, message return karta hai

**5 Risk Levels**:
1. 🟢 Normal (0-20%)
2. 🟡 Mild (20-40%)
3. 🟠 Moderate (40-60%)
4. 🔴 High (60-80%)
5. 🚨 Critical (80-100%)

**Why detailed levels**:
- Better granularity
- Clear urgency communication
- Color-coded for quick understanding

---

**Lines 64-70: Step State Management**
```python
def patient_form():
    if "step" not in st.session_state:
        st.session_state.step = "language"
```

**Kya kar raha hai**: Multi-step form ka state manage kar raha hai

**Steps**:
1. `"language"`: Language selection
2. `"personal"`: Name & mobile
3. `"medical"`: Health assessment

---

**Lines 75-90: Step 1 - Language Selection**
```python
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
```

**Kya kar raha hai**:
- Bilingual language choice dikha raha hai
- Selection ko session state mein save kar raha hai
- Next step par navigate kar raha hai
- `st.rerun()` se page refresh hota hai

**Why `return`**: 
- Baaki code execute nahi hona chahiye
- Only language selection UI show hona chahiye

---

**Lines 98-124: Step 2 - Personal Details**
```python
if st.session_state.step == "personal":
    name = st.text_input(T["full_name"]).strip()
    mobile = st.text_input(T["mobile"]).strip()
    
    mobile_valid = re.match(r"^[6-9]\d{9}$", mobile)
    
    if st.button(T["proceed"], use_container_width=True):
        if not name or not mobile_valid:
            st.error("Please enter valid details...")
        else:
            st.session_state.name = name
            st.session_state.mobile = mobile
            st.session_state.step = "medical"
            st.rerun()
```

**Kya kar raha hai**:
- Name aur mobile input le raha hai
- Mobile number validate kar raha hai
- Valid data session state mein save kar raha hai

**Mobile Validation Regex**: `^[6-9]\d{9}$`
- `^`: Start of string
- `[6-9]`: First digit 6, 7, 8, or 9
- `\d{9}`: Exactly 9 more digits
- `$`: End of string
- **Total**: 10 digits, starts with 6-9 (Indian mobile format)

**`.strip()`**: Leading/trailing spaces remove karta hai

---

**Lines 129-148: Step 3 Header - Patient ID**
```python
if st.session_state.step == "medical":
    if "patient_id" not in st.session_state:
        st.session_state.patient_id = generate_patient_id()
    
    st.text_input(
        T["patient_id"],
        value=st.session_state.patient_id,
        disabled=True
    )
```

**Kya kar raha hai**:
- Patient ID generate kar raha hai (once)
- Disabled text input mein display kar raha hai

**Why disabled**: User edit nahi kar sakta

---

**Lines 153-164: Basic Info Inputs**
```python
col1, col2 = st.columns(2)
with col1:
    gender = st.radio(T["gender"], ["Male", "Female"], horizontal=True)
with col2:
    age = st.slider(T["age"], 18, 90, 35)
```

**Kya kar raha hai**:
- 2 columns create kar raha hai
- Gender radio buttons (horizontal)
- Age slider (18-90 range, default 35)

**Why columns**: Better space utilization

---

**Lines 169-187: Medical History**
```python
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
```

**Kya kar raha hai**:
- Yes/No radio buttons for hypertension & heart disease
- Dropdown for smoking history
- Language-specific options

**Smoking Options**:
- English: Never, Former, Occasional, Current
- Hindi: कभी नहीं, पहले करता था, कभी-कभी, वर्तमान

---

**Lines 192-201: Clinical Measurements**
```python
bmi = st.slider("BMI", 10.0, 50.0, 25.0)
hba1c = st.slider("HbA1c (%)", 4.0, 15.0, 5.6)
glucose = st.slider("Blood Glucose (mg/dL)", 70, 300, 120)
```

**Kya kar raha hai**: Three sliders for clinical values

**Ranges**:
- **BMI**: 10-50 (default 25)
  - < 18.5: Underweight
  - 18.5-24.9: Normal
  - 25-29.9: Overweight
  - ≥ 30: Obese

- **HbA1c**: 4-15% (default 5.6)
  - < 5.7%: Normal
  - 5.7-6.4%: Prediabetes
  - ≥ 6.5%: Diabetes

- **Glucose**: 70-300 mg/dL (default 120)
  - 70-100: Normal fasting
  - 100-125: Prediabetes
  - ≥ 126: Diabetes

---

**Lines 206-250: Submit & Prediction**
```python
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
    
    # Save to database
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO patient_records
    (patient_id, name, mobile, language, gender, age,
     hypertension, heart_disease, smoking_history,
     bmi, hba1c, glucose, risk_probability, risk_category)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (...))
    conn.commit()
    conn.close()
```

**Kya kar raha hai**:
1. Patient data dictionary banata hai
2. ML model se risk predict karta hai
3. Database mein save karta hai

**Data Transformations**:
- `"Yes"/"No"` → `1/0` (binary)
- `smoking_ui.lower()` → lowercase string
- `prob` → float (0-1)

**SQL Parameterized Query**:
- `?` placeholders SQL injection prevent karte hain
- Values tuple mein pass hote hain

---

**Lines 255-262: Result Display**
```python
st.markdown(f"""
<div class="card" style="border-left:6px solid {risk_ui['color']}">
    <h2>{risk_ui['emoji']} {risk_ui['label']}</h2>
    <p><b>{T['risk_result']}:</b> {prob*100:.2f}%</p>
    <p><b>Urgency:</b> {risk_ui['urgency']}</p>
    <p>{risk_ui['message']}</p>
</div>
""", unsafe_allow_html=True)
```

**Kya kar raha hai**:
- Color-coded border dikha raha hai
- Emoji + label
- Risk percentage
- Urgency level
- Actionable message

**Dynamic Styling**: `border-left:6px solid {risk_ui['color']}`
- Green for low risk
- Yellow for mild
- Red for high

---

**Lines 267-288: AI Explanation**
```python
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
        "AI explanation temporarily unavailable..."
        if st.session_state.language == "English"
        else "AI जानकारी उपलब्ध नहीं है..."
    )
```

**Kya kar raha hai**:
- GenAI/Rule-based explanation try karta hai
- Exception hone par fallback message dikha raha hai
- Language-specific error messages

**Why try-except**:
- API down ho sakti hai
- Internet issue ho sakta hai
- Graceful degradation

---

**Lines 293-295: Session Cleanup**
```python
for key in ["step", "patient_id", "name", "mobile", "language"]:
    if key in st.session_state:
        del st.session_state[key]
```

**Kya kar raha hai**: 
- Form submission ke baad session state clean kar raha hai
- Next patient ke liye fresh start

**Why delete**: 
- Memory leaks prevent
- Data privacy
- Clean state for next patient

---

### 1️⃣1️⃣ ui/doctor_dashboard.py - Doctor's Clinical Dashboard

**Lines 39-44: Load Patient Data**
```python
conn = get_connection()
df = pd.read_sql(
    "SELECT * FROM patient_records ORDER BY created_at DESC",
    conn
)
conn.close()
```

**Kya kar raha hai**:
- Database se sab patient records load kar raha hai
- Latest records first (DESC order)
- Pandas DataFrame mein convert kar raha hai

**Why Pandas**:
- Easy data manipulation
- Built-in plotting
- DataFrame se Streamlit table easily ban jata hai

---

**Lines 63-64: Display All Records**
```python
st.dataframe(df, width="stretch")
```

**Kya kar raha hai**: 
- Interactive table dikha raha hai
- Full width use kar raha hai
- Sortable columns
- Scrollable

---

**Lines 76-80: Patient Selection**
```python
patient_ids = df["patient_id"].unique().tolist()
selected_patient = st.selectbox(T["select_patient"], patient_ids)

patient_df = df[df["patient_id"] == selected_patient].sort_values("created_at")
latest = patient_df.iloc[-1]
```

**Kya kar raha hai**:
1. Unique patient IDs extract kar raha hai
2. Dropdown mein dikha raha hai
3. Selected patient ke sab records filter kar raha hai
4. Latest record extract kar raha hai

**`.iloc[-1]`**: Last row (latest record)

---

**Lines 91-100: Risk Overview Cards**
```python
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(T["patient_id"], latest["patient_id"])
with col2:
    st.metric(
        "Risk Probability",
        f"{latest['risk_probability']*100:.2f}%"
    )
with col3:
    st.metric(T["risk_category"], latest["risk_category"])
```

**Kya kar raha hai**: 
- 3 metric cards dikha raha hai
- Patient ID, Risk %, Risk Category

**st.metric()**: 
- Big number display
- Delta (change) bhi dikha sakta hai
- Professional looking cards

---

**Lines 111-142: Trend Charts**
```python
if len(patient_df) > 1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.line_chart(
            patient_df.set_index("created_at")["risk_probability"] * 100
        )
    
    with col2:
        st.line_chart(
            patient_df.set_index("created_at")["hba1c"]
        )
    
    st.line_chart(
        patient_df.set_index("created_at")["bmi"]
    )
else:
    st.info("Not enough historical data to show trends.")
```

**Kya kar raha hai**:
- Multiple records hain to trend charts dikha raha hai
- Time-series line charts
- Risk, HbA1c, BMI trends

**Why `if len(patient_df) > 1`**:
- Trend dikhane ke liye kam se kam 2 data points chahiye
- Single record mein trend nahi dikhega

**`.set_index("created_at")`**: 
- X-axis par date/time dikha raha hai
- Time-series chart ban jata hai

---

**Lines 160-178: AI Clinical Explanation**
```python
patient_data = {
    "gender": latest["gender"],
    "age": latest["age"],
    # ... all fields
}

ai_explanation = explain(
    patient_data=patient_data,
    risk=latest["risk_category"],
    prob=latest["risk_probability"],
    audience="clinician"
)

st.write(ai_explanation)
```

**Kya kar raha hai**:
- Latest record se patient data extract kar raha hai
- Clinician audience ke liye explanation generate kar raha hai
- Medical terminology use hoga

---

**Lines 189-191: Next Steps**
```python
steps = next_steps(latest["risk_category"])
for step in steps:
    st.write("•", step)
```

**Kya kar raha hai**:
- Clinical action items get kar raha hai
- Bullet points mein dikha raha hai

---

**Lines 204-222: PDF Report Generation**
```python
if st.button("📥 Generate & Download PDF Report..."):
    pdf_path = generate_pdf(
        latest.to_dict(),
        ai_explanation
    )
    
    with open(pdf_path, "rb") as f:
        st.download_button(
            label=T["download_pdf"],
            data=f,
            file_name=f"{latest['patient_id']}_report.pdf",
            mime="application/pdf"
        )
```

**Kya kar raha hai**:
1. Button click par PDF generate karta hai
2. File read karta hai (binary mode)
3. Download button dikha raha hai

**`latest.to_dict()`**: 
- Pandas Series ko dictionary mein convert karta hai

**`"rb"`**: 
- Read binary mode
- PDF binary file hai

**Why separate button**:
- PDF generation slow ho sakta hai
- On-demand generation
- User control

---

### 1️⃣2️⃣ ui/landing.py - Home Page

```python
def landing_page():
    st.title("🏥 Preventive Clinical Decision Support System")
    
    st.markdown("""
    ### Welcome to AI-powered Diabetes Risk Assessment
    
    This system helps in:
    - Early diabetes risk screening
    - Clinical decision support for doctors
    - Personalized health recommendations
    - Multi-language support (English & Hindi)
    
    **For Patients**: Take a quick health assessment
    **For Doctors**: Monitor patient trends and generate reports
    """)
    
    st.info("👈 Use the sidebar to navigate")
```

**Kya kar raha hai**: Simple welcome page dikha raha hai

---

### 1️⃣3️⃣ ui/login.py - Doctor Authentication

```python
def login_page():
    st.markdown("## 🔐 Doctor Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login", use_container_width=True):
        if username == "doctor" and password == "admin123":
            st.session_state.doctor = username
            st.session_state.page = "Doctor Dashboard"
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")
```

**Kya kar raha hai**:
- Username/password input le raha hai
- Hardcoded credentials check kar raha hai
- Session state mein doctor save kar raha hai

**Security Issues** (Current):
- Plaintext password
- Hardcoded credentials
- No encryption
- No multi-user support

**Production Recommendations**:
- Database mein hashed passwords
- JWT tokens
- Multi-factor authentication
- Role-based access control

---

### 1️⃣4️⃣ ui/styles.py - CSS Styling

```python
def apply_styles():
    st.markdown("""
    <style>
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
    
    /* More styles... */
    </style>
    """, unsafe_allow_html=True)
```

**Kya kar raha hai**: 
- Reusable CSS classes define kar raha hai
- Consistent UI theme

**Key Classes**:
- `.card`: White background containers
- `.section-title`: Blue headings
- `.helper`: Gray helper text

---

## 📂 TRAINING FILES

### 1️⃣5️⃣ train/train_model.py - Model Training

**Complete Flow**:

```python
# Step 1: Load data
df = pd.read_csv("../data/diabetes_dataset.csv")

# Step 2: Separate features and target
X = df.drop(columns=["diabetes"])
y = df["diabetes"]

# Step 3: One-hot encode categorical variables
X_encoded = pd.get_dummies(X)
feature_names = X_encoded.columns.tolist()

# Step 4: Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

# Step 5: Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 6: Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# Step 7: Evaluate
y_prob = model.predict_proba(X_test_scaled)[:, 1]
print("ROC-AUC:", roc_auc_score(y_test, y_prob))

# Step 8: Save everything
with open("model.pkl", "wb") as f:
    pickle.dump((model, scaler, feature_names), f)
```

**Step-by-Step Breakdown**:

**Step 1**: CSV se data load
- 100K+ rows
- 9 columns (8 features + 1 target)

**Step 2**: Features aur target alag kar diye
- X: Input features
- y: Output (diabetes: 0/1)

**Step 3**: `pd.get_dummies()`
- Categorical → Binary columns
- Example: `gender: Male` → `gender_Male: 1, gender_Female: 0`
- `smoking_history: current` → `smoking_history_current: 1, others: 0`

**Step 4**: `train_test_split()`
- 80% training data
- 20% testing data
- `random_state=42`: Reproducible split

**Step 5**: `StandardScaler`
- Mean = 0, Std = 1
- Helps model converge faster
- All features same scale par aate hain

**Step 6**: `LogisticRegression`
- Binary classifier
- Probability output
- `max_iter=1000`: Training iterations

**Step 7**: `ROC-AUC Score`
- Model quality measure
- 0.5 = random guessing
- 1.0 = perfect
- Typical good score: > 0.75

**Step 8**: Pickle dump
- Model + Scaler + Features ek saath
- Ensures prediction consistency

---

### 1️⃣6️⃣ train/preprocess.py - Data Preprocessing

```python
import pandas as pd

def clean_data(df):
    """
    Remove missing values and outliers
    """
    # Drop missing
    df = df.dropna()
    
    # Remove outliers (BMI example)
    df = df[(df['bmi'] >= 10) & (df['bmi'] <= 50)]
    
    # Standardize smoking history
    smoking_map = {
        'No Info': 'never',
        'never': 'never',
        'current': 'current',
        'former': 'former',
        'occasional': 'occasional'
    }
    df['smoking_history'] = df['smoking_history'].map(smoking_map)
    
    return df
```

**Kya kar raha hai**:
- Missing values remove kar raha hai
- Outliers filter kar raha hai
- Inconsistent values standardize kar raha hai

**Why preprocessing**:
- Clean data → Better model
- Consistent format → Reliable predictions
- Outliers remove → Model robust

---

## 🎯 CODE QUALITY & BEST PRACTICES

### ✅ Good Practices Used

1. **Modular Code**
   - Separate files for separate concerns
   - Reusable functions

2. **Error Handling**
   - Try-except blocks
   - Fallback mechanisms

3. **Type Hints** (in some places)
   - `patient_record: dict`
   - Better code documentation

4. **Comments**
   - Descriptive docstrings
   - Inline explanations

5. **Session Management**
   - Clean session cleanup
   - State tracking

6. **Multi-language Support**
   - Internationalization
   - User-friendly

---

### ⚠️ Areas for Improvement

1. **Security**
   - Hardcoded credentials
   - No encryption
   - SQL injection (though using parameterized queries)

2. **Testing**
   - No unit tests
   - No integration tests

3. **Logging**
   - No error logging
   - No audit trails

4. **Configuration**
   - Hardcoded values
   - No config file

5. **Scalability**
   - SQLite not for production
   - No caching
   - No load balancing

---

## 🔍 TECHNICAL DECISIONS EXPLAINED

### Why Logistic Regression?
- **Interpretable**: Feature coefficients visible
- **Fast**: Quick training & prediction
- **Proven**: Medical field mein widely used
- **Probability output**: Not just yes/no

### Why SQLite?
- **Simple**: No server setup
- **Portable**: Single file
- **Good for MVP**: Prototyping ke liye perfect
- **Later migration easy**: To PostgreSQL/MySQL

### Why Streamlit?
- **Rapid development**: Hours mein UI ready
- **Python-native**: No JavaScript needed
- **Interactive**: Real-time updates
- **Deployment easy**: Streamlit Cloud

### Why Hybrid AI?
- **Reliability**: Rule-based always works
- **Quality**: GenAI better explanations
- **Cost**: API calls only when needed
- **Transparency**: Medical safety

---

## 📊 DATA FLOW DIAGRAM

```
Patient Input (Form)
        ↓
Data Validation
        ↓
Feature Engineering (One-hot, Scaling)
        ↓
ML Model Prediction
        ↓
Risk Categorization
        ↓
AI Explanation Generation
        ↓
Database Storage
        ↓
UI Display + PDF Report
```

---

## 🔄 SESSION STATE FLOW

```
App Start
    ↓
session_state.page = "Home"
    ↓
User clicks "Patient Assessment"
    ↓
session_state.step = "language"
    ↓
Language selected
    ↓
session_state.language = "Hindi"
session_state.step = "personal"
    ↓
Name/Mobile entered
    ↓
session_state.name, mobile saved
session_state.step = "medical"
    ↓
Form submitted
    ↓
session_state cleared
```

---

## 🎓 KEY LEARNINGS

### What This Code Teaches:

1. **End-to-end ML Application**
   - Data → Model → Deployment

2. **Healthcare AI**
   - Responsible AI
   - Safety measures
   - Explainability

3. **Full-stack Python**
   - Backend logic
   - Frontend UI
   - Database operations

4. **Real-world Considerations**
   - Multi-language
   - Error handling
   - User experience

---

**Yeh document har file ka detailed explanation hai. Har line kya kar rahi hai aur kyu use ho rahi hai, sab clear hai.**
