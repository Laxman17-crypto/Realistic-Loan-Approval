from src.data_preprocessing import engineer_features
import pandas as pd
import pytest

def test_engineer_features_creates_ratios():
    df = pd.DataFrame({
        "annual_income": [60000],
        "current_debt": [15000],
        "loan_amount": [20000]
    })
    
    out = engineer_features(df.copy())
    assert "debt_to_income_ratio" in out.columns
    assert "loan_to_income_ratio" in out.columns
    # numeric correctness
    assert out.loc[0, "debt_to_income_ratio"] == pytest.approx(15000 / 60000)
    assert out.loc[0, "loan_to_income_ratio"] == pytest.approx(20000 / 60000)