# 🏥 Health Risk Predictor - Diabetes Risk Assessment System

## 📋 Project Overview

**Health Risk Predictor** ek AI-based Clinical Decision Support System hai jo diabetes risk assessment karta hai. Yeh system Machine Learning aur Generative AI ka use karke patients ki health data analyze karta hai aur doctors ko clinical decision-making mein help karta hai.

### ✨ Main Features

1. **Multi-language Support** - English aur Hindi dono languages support karta hai
2. **AI-Powered Risk Prediction** - Machine Learning model se diabetes risk predict karta hai
3. **Doctor Dashboard** - Doctors ke liye patient monitoring aur trend analysis
4. **PDF Report Generation** - Professional medical reports generate karta hai
5. **GenAI Explanations** - Google Gemini AI se health explanations milte hain
6. **Secure Authentication** - Doctor login system
7. **Database Storage** - Patient records SQLite database mein save hote hain

---

## 🏗️ Project Structure

```
health-risk-predictor/
│
├── app.py                          # Main application entry point
├── auth.py                         # Doctor authentication module
├── requirements.txt                # Python dependencies
├── .env                           # API keys aur environment variables
│
├── core/                          # Core business logic
│   ├── __init__.py
│   ├── db.py                      # Database operations
│   ├── risk_engine.py             # ML model risk prediction
│   ├── genai_explainer.py         # AI explanation generation
│   ├── llm_engine.py              # Google Gemini AI integration
│   ├── decision_support.py        # Clinical decision recommendations
│   ├── pdf_report.py              # PDF generation
│   ├── i18n.py                    # Language translation
│   ├── explainability.py          # Model explainability
│   ├── explanations.py            # Explanation templates
│   ├── severity_engine.py         # Risk severity calculation
│   ├── risk_utils.py              # Risk utility functions
│   └── utils.py                   # Common utilities
│
├── ui/                            # User Interface components
│   ├── __init__.py
│   ├── landing.py                 # Home page
│   ├── patient_form.py            # Patient assessment form
│   ├── doctor_dashboard.py        # Doctor's dashboard
│   ├── login.py                   # Login page
│   ├── layout.py                  # Layout components
│   └── styles.py                  # CSS styling
│
├── train/                         # ML Model training
│   ├── diabetes_dataset.csv       # Training dataset (100K+ records)
│   ├── train_model.py             # Model training script
│   ├── preprocess.py              # Data preprocessing
│   └── model.pkl                  # Trained model file
│
├── data/                          # Data storage
│   ├── clinical.db                # SQLite database
│   └── *.pdf                      # Generated reports
│
├── reports/                       # Generated PDF reports folder
│   └── *.pdf
│
└── pages/                         # Additional Streamlit pages
    └── 4_Disease_Cards.py         # Disease information cards
```

---

## 🔧 Technology Stack

### Backend
- **Python 3.11+**
- **Streamlit** - Web application framework
- **Scikit-learn** - Machine Learning
- **Pandas & NumPy** - Data processing
- **SQLite3** - Database

### AI/ML
- **Logistic Regression** - Diabetes prediction model
- **Google Gemini AI** - Natural language explanations
- **StandardScaler** - Feature scaling

### Reporting
- **ReportLab** - PDF generation
- **Matplotlib/Plotly** - Data visualization (optional)

---

## 🚀 Installation & Setup

### 1. Prerequisites
```bash
Python 3.11 ya usse higher
pip (Python package manager)
```

### 2. Clone/Extract Project
```bash
cd health-risk-predictor
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
`.env` file create karo aur apna Google Gemini API key add karo:

```env
GEMINI_API_KEY=your_api_key_here
```

**Note:** API key lene ke liye: https://ai.google.dev/

### 5. Initialize Database
Database automatically initialize ho jata hai jab app first time run hoti hai.

### 6. Run Application
```bash
streamlit run app.py
```

Application `http://localhost:8501` par open hogi.

---

## 📊 How It Works - System Flow

### 1️⃣ **Patient Journey**

```
Language Selection (English/Hindi)
        ↓
Personal Details Entry (Name, Mobile)
        ↓
Health Assessment Form
   - Basic Info (Gender, Age)
   - Medical History (Hypertension, Heart Disease, Smoking)
   - Clinical Measurements (BMI, HbA1c, Glucose)
        ↓
Risk Prediction (ML Model)
        ↓
AI Explanation Generation
        ↓
Database Storage
```

### 2️⃣ **Doctor Journey**

```
Doctor Login
        ↓
Patient Records Dashboard
        ↓
Select Patient
        ↓
View Risk Trends & History
        ↓
AI Clinical Explanation
        ↓
Download PDF Report
```

---

## 🧠 Machine Learning Model Details

### Model Type
**Logistic Regression Classifier**

### Features Used (8 total)
1. **Gender** - Male/Female (categorical)
2. **Age** - 18-90 years (numerical)
3. **Hypertension** - 0/1 (binary)
4. **Heart Disease** - 0/1 (binary)
5. **Smoking History** - Never/Former/Occasional/Current (categorical)
6. **BMI** - Body Mass Index (numerical)
7. **HbA1c** - Glycated Hemoglobin % (numerical)
8. **Blood Glucose** - mg/dL (numerical)

### Model Performance
- **ROC-AUC Score**: Model ki accuracy measure karta hai
- **Training Data**: 100,000+ patient records
- **Preprocessing**: 
  - One-hot encoding for categorical variables
  - StandardScaler for numerical features
  - Train-test split: 80-20

### Risk Categories
- **Low Risk**: < 30% probability
- **Moderate Risk**: 30-60% probability
- **High Risk**: > 60% probability

### Risk UI Levels (More Detailed)
- 🟢 **Normal** (0-20%): No immediate risk
- 🟡 **Mild Risk** (20-40%): Early risk detected
- 🟠 **Moderate Risk** (40-60%): Regular monitoring advised
- 🔴 **High Risk** (60-80%): Doctor consultation needed
- 🚨 **Critical Risk** (80-100%): Immediate medical attention

---

## 🗄️ Database Schema

### Table: `patient_records`

| Column Name        | Data Type | Description                          |
|-------------------|-----------|--------------------------------------|
| id                | INTEGER   | Primary key (auto-increment)         |
| patient_id        | TEXT      | Unique patient identifier            |
| name              | TEXT      | Patient full name                    |
| mobile            | TEXT      | 10-digit mobile number               |
| language          | TEXT      | English/Hindi                        |
| gender            | TEXT      | Male/Female                          |
| age               | INTEGER   | Patient age                          |
| hypertension      | INTEGER   | 0 or 1                              |
| heart_disease     | INTEGER   | 0 or 1                              |
| smoking_history   | TEXT      | Smoking status                       |
| bmi               | REAL      | Body Mass Index                      |
| hba1c             | REAL      | HbA1c level                         |
| glucose           | REAL      | Blood glucose level                  |
| risk_probability  | REAL      | Predicted risk (0-1)                |
| risk_category     | TEXT      | Low/Moderate/High                    |
| created_at        | TIMESTAMP | Record creation time                 |

---

## 📁 File-wise Detailed Explanation

### 🔹 Core Files

#### 1. **app.py** - Main Application
**Purpose**: Application ka entry point aur page routing

**Key Functions**:
- Streamlit configuration
- Database initialization
- Session state management
- Navigation sidebar
- Page routing logic

**Code Flow**:
```python
1. Import all UI modules
2. Initialize database
3. Setup session state
4. Create sidebar navigation
5. Route to appropriate page based on selection
```

---

#### 2. **core/db.py** - Database Module
**Purpose**: SQLite database operations

**Key Functions**:
- `init_db()` - Database aur tables create karta hai
- `get_connection()` - Database connection return karta hai

**Database Path**: `data/clinical.db`

**Why SQLite?**
- Lightweight
- No server setup needed
- Perfect for small-medium applications

---

#### 3. **core/risk_engine.py** - Risk Prediction Engine
**Purpose**: ML model ko load karke risk predict karta hai

**Key Functions**:
- `compute_risk(patient_data)` - Risk probability calculate karta hai

**Process**:
```python
1. Load trained model, scaler, features from pickle file
2. Convert patient data to DataFrame
3. One-hot encode categorical variables
4. Scale features using StandardScaler
5. Predict probability using model
6. Categorize risk as Low/Moderate/High
7. Return probability, risk category, model, features
```

**Why Pickle?**
Model, scaler, aur feature names ek saath save hote hain taaki prediction consistent rahe.

---

#### 4. **core/genai_explainer.py** - AI Explanation Engine
**Purpose**: Dual-mode explanation system

**Two Modes**:
1. **Rule-based** (Always available - Fallback)
   - Deterministic medical logic
   - No API dependency
   - Clinical guidelines based

2. **GenAI** (Premium experience)
   - Google Gemini AI powered
   - Natural language explanations
   - Context-aware recommendations

**Key Functions**:
- `_rule_based_summary()` - Clinical rule-based insights
- `explain()` - Hybrid explanation with fallback

**Why Hybrid?**
- Reliability: Rule-based hamesha kaam karta hai
- Enhancement: GenAI better explanations deta hai
- Fail-safe: API failure pe bhi system work karta hai

---

#### 5. **core/llm_engine.py** - Google Gemini Integration
**Purpose**: Generative AI se explanations generate karna

**Key Functions**:
- `generate_llm_explanation()` - Gemini API call

**Features**:
- Audience-specific prompts (Patient/Clinician)
- Medical safety guidelines
- Context-aware responses

**Prompt Structure**:
```
- Medical responsibility
- Patient data context
- Risk level
- Audience type
- Safety rules (no diagnosis)
```

---

#### 6. **core/pdf_report.py** - PDF Report Generator
**Purpose**: Professional medical reports generate karna

**Library**: ReportLab

**Report Sections**:
1. Header (Title + Subtitle)
2. Patient Details
3. Clinical Measurements
4. Risk Results
5. AI Explanation
6. Medical Disclaimer
7. Timestamp

**Multi-language**: English aur Hindi dono support

**Why ReportLab?**
- Professional PDF creation
- Customizable layouts
- Medical report standards compliance

---

#### 7. **core/i18n.py** - Internationalization
**Purpose**: Multi-language support

**Supported Languages**:
- English
- Hindi (Devanagari script)

**Translation Dictionary**:
- UI labels
- Medical terms
- Instructions
- Messages

**Function**: `get_text(language)` - Language-specific text return karta hai

---

#### 8. **core/decision_support.py** - Clinical Decision Support
**Purpose**: Risk category based clinical recommendations

**Recommendations by Risk**:

**High Risk**:
- Confirmatory lab tests
- 3-month follow-up
- Lifestyle counseling
- Specialist referral

**Moderate Risk**:
- Lifestyle modification
- 6-month screening
- Regular monitoring

**Low Risk**:
- Annual screening
- Healthy lifestyle maintenance

---

### 🔹 UI Files

#### 9. **ui/patient_form.py** - Patient Assessment Form
**Purpose**: Patient se health data collect karna

**Three-Step Process**:

**Step 1: Language Selection**
- English/Hindi choice

**Step 2: Personal Details**
- Name validation
- Mobile number validation (10 digits, starts with 6-9)

**Step 3: Medical Form**
- Patient ID generation
- Basic info collection
- Medical history
- Clinical measurements
- Risk prediction
- Database storage
- Result display

**Risk UI Function**:
```python
get_risk_ui(prob):
    Returns emoji, color, message, urgency based on probability
```

---

#### 10. **ui/doctor_dashboard.py** - Doctor Dashboard
**Purpose**: Doctor ke liye patient monitoring system

**Features**:

1. **All Patient Records Table**
   - Sortable by date
   - Complete patient list

2. **Patient Selection**
   - Dropdown to select patient

3. **Risk Overview Cards**
   - Patient ID
   - Risk probability
   - Risk category

4. **Trend Analysis**
   - Diabetes risk over time (Line chart)
   - HbA1c trend
   - BMI trend

5. **AI Clinical Explanation**
   - Clinician-specific language
   - Medical terminology

6. **Recommended Next Steps**
   - Evidence-based recommendations

7. **PDF Report Download**
   - One-click report generation

**Why Dashboard?**
Doctors ko patient ki complete history aur trends ek jagah dikhana

---

#### 11. **ui/landing.py** - Home Page
**Purpose**: Welcome page aur system introduction

**Content**:
- Project title
- Purpose description
- Navigation instructions
- Key features highlight

---

#### 12. **ui/login.py** - Doctor Login
**Purpose**: Doctor authentication

**Default Credentials**:
```
Username: doctor
Password: admin123
```

**Security Note**: Production mein better authentication use karna chahiye

---

#### 13. **ui/styles.py** - CSS Styling
**Purpose**: Consistent UI styling

**Styling Elements**:
- Card designs
- Color schemes
- Typography
- Spacing

---

### 🔹 Training Files

#### 14. **train/train_model.py** - Model Training Script
**Purpose**: ML model ko train karna

**Process**:
```python
1. Load diabetes_dataset.csv
2. Split features and target
3. One-hot encode categorical variables
4. Train-test split (80-20)
5. StandardScaler normalization
6. Train Logistic Regression
7. Calculate ROC-AUC score
8. Save model + scaler + features to pickle
```

**Output**: `model.pkl` file

**To Retrain**:
```bash
cd train
python train_model.py
```

---

#### 15. **train/diabetes_dataset.csv** - Training Dataset
**Size**: 100,000+ patient records

**Columns**:
- gender
- age
- hypertension
- heart_disease
- smoking_history
- bmi
- HbA1c_level
- blood_glucose_level
- **diabetes** (target variable: 0/1)

**Data Quality**:
- Real-world medical data patterns
- Balanced classes (diabetic/non-diabetic)
- Multiple risk factors covered

---

#### 16. **train/preprocess.py** - Data Preprocessing
**Purpose**: Data cleaning aur transformation utilities

**Functions**:
- Missing value handling
- Outlier detection
- Feature engineering
- Data validation

---

### 🔹 Other Files

#### 17. **auth.py** - Authentication Module
**Purpose**: User authentication logic

**Functions**:
- Doctor login verification
- Session management
- Access control

---

#### 18. **pages/4_Disease_Cards.py** - Disease Information
**Purpose**: Educational content about diseases

**Content**:
- Diabetes information
- Risk factors
- Prevention tips
- Symptoms

---

#### 19. **requirements.txt** - Dependencies
```txt
streamlit          # Web framework
pandas             # Data manipulation
numpy              # Numerical computing
scikit-learn       # Machine learning
reportlab          # PDF generation
python-dotenv      # Environment variables
google-genai       # Google Gemini AI
```

---

## 🎯 Key Technical Decisions & Rationale

### 1. **Why Streamlit?**
- Rapid prototyping
- Python-native
- No frontend coding needed
- Built-in widgets
- Easy deployment

### 2. **Why Logistic Regression?**
- Interpretable
- Fast training
- Good for binary classification
- Medical field mein trusted
- Feature importance visible

### 3. **Why SQLite?**
- Zero configuration
- Single file database
- Perfect for prototypes
- Easy to backup

### 4. **Why Hybrid AI Approach?**
- **Rule-based**: Always reliable
- **GenAI**: Better UX
- **Fallback**: System never fails

### 5. **Why Multi-language?**
- India mein Hindi speakers bhi bohot hain
- Healthcare accessibility
- Better patient engagement

---

## 🔒 Security Considerations

### Current Implementation
- Basic doctor authentication
- Session-based access control
- Data stored locally

### Production Recommendations
1. **Use proper authentication** (OAuth, JWT)
2. **Encrypt sensitive data**
3. **HTTPS deployment**
4. **Input sanitization**
5. **Rate limiting**
6. **Audit logging**
7. **HIPAA compliance** (if in US)
8. **Data privacy regulations**

---

## 🚨 Medical Disclaimer

**IMPORTANT**: This system is for **educational and screening purposes only**.

- ❌ NOT a diagnostic tool
- ❌ NOT a replacement for professional medical advice
- ✅ Decision support aid only
- ✅ Must be reviewed by qualified healthcare professionals

---

## 📈 Future Enhancements

### Short-term
1. ✅ Add more disease models (CVD, Hypertension)
2. ✅ Email/SMS notifications
3. ✅ Export to Excel
4. ✅ Better visualizations

### Long-term
1. ✅ Mobile app
2. ✅ Cloud deployment
3. ✅ Integration with EHR systems
4. ✅ Real-time monitoring
5. ✅ Multi-tenant support
6. ✅ Advanced ML models (Deep Learning)

---

## 🐛 Common Issues & Solutions

### Issue 1: Model not found
**Solution**: 
```bash
cd train
python train_model.py
```

### Issue 2: Database error
**Solution**: Delete `data/clinical.db` and restart app

### Issue 3: API key error
**Solution**: Check `.env` file for correct `GEMINI_API_KEY`

### Issue 4: Port already in use
**Solution**: 
```bash
streamlit run app.py --server.port 8502
```

---

## 👨‍💻 Development Guidelines

### Code Style
- PEP 8 compliance
- Clear variable names
- Comments in English
- Docstrings for functions

### Testing
```bash
# Run basic checks
python -m pytest tests/
```

### Git Workflow
```bash
git checkout -b feature-name
# Make changes
git commit -m "Description"
git push origin feature-name
```

---

## 📞 Support & Contact

### For Bugs/Issues
Create an issue on GitHub repository

### For Feature Requests
Submit a pull request with detailed description

### Documentation
Check project wiki for detailed guides

---

## 📜 License

This project is for **educational purposes**. 

Medical applications require proper licensing and regulatory approvals before production use.

---

## 🙏 Acknowledgments

- **Dataset**: Diabetes dataset from healthcare research
- **Google Gemini AI**: For natural language generation
- **Streamlit**: For amazing web framework
- **Open Source Community**: For libraries and tools

---

## 📚 References

1. American Diabetes Association Guidelines
2. WHO Diabetes Fact Sheets
3. Scikit-learn Documentation
4. Google Gemini AI Documentation
5. Clinical Decision Support Systems Research Papers

---

## ⚡ Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Train model (optional, already trained)
cd train && python train_model.py

# Run application
streamlit run app.py

# Access at
http://localhost:8501
```

---

**Made with ❤️ for Healthcare Innovation**

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Python Version**: 3.11+  
**Status**: Educational Prototype
