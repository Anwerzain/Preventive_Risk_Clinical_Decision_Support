import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

DATA_PATH = "../data/diabetes_dataset.csv"
MODEL_PATH = "model.pkl"

df = pd.read_csv(DATA_PATH)

TARGET_COL = "diabetes"

X = df.drop(columns=[TARGET_COL])
y = df[TARGET_COL]

# One-hot encoding
X_encoded = pd.get_dummies(X)

feature_names = X_encoded.columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

y_prob = model.predict_proba(X_test_scaled)[:, 1]
print("ROC-AUC:", roc_auc_score(y_test, y_prob))

# 🔥 SAVE EVERYTHING TOGETHER
with open(MODEL_PATH, "wb") as f:
    pickle.dump((model, scaler, feature_names), f)

print("✅ Model saved correctly at train/model.pkl")
