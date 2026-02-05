import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

TARGET_COL = "diabetes"

def load_and_preprocess(csv_path):
    df = pd.read_csv(csv_path)

    # Drop missing values
    df = df.dropna()

    # Separate target
    y = df[TARGET_COL]
    X = df.drop(TARGET_COL, axis=1)

    # One-hot encode categorical columns
    X = pd.get_dummies(X, columns=["gender", "smoking_history"], drop_first=True)

    # Scale numerical features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    return X_train, X_test, y_train, y_test, scaler, X.columns.tolist()
