import pandas as pd
import numpy as np
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler

NUMERIC_COLS=['age','years_employed','annual_income',
  'credit_score','credit_history_years','savings_assets',
  'current_debt','defaults_on_file','delinquencies_last_2yrs',
  'derogatory_marks','loan_amount','interest_rate',
  'debt_to_income_ratio','loan_to_income_ratio']

CATEGORICAL_COLS = ["occupation_status", "loan_intent", "product_type"]

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    # Guard against division by zero
    df = df.copy()
    df["debt_to_income_ratio"] = df["current_debt"] / (df["annual_income"] + 1e-9)
    df["loan_to_income_ratio"] = df["loan_amount"] / (df["annual_income"] + 1e-9)

    return df

def create_preprocessor() -> ColumnTransformer:
    """Return a ColumnTransformer that encodes categorical cols and scales numeric cols."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_COLS),
            ("num", StandardScaler(), NUMERIC_COLS)
        ],
        remainder="drop"
    )
    return preprocessor

def save_preprocessor(preprocessor, path="models/preprocessor.joblib"):
    joblib.dump(preprocessor, path)

def load_preprocessor(path="models/preprocessor.joblib"):
    return joblib.load(path)    