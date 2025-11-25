from src.data_preprocessing import create_preprocessor, engineer_features
import pandas as pd

def test_preprocessor_transforms_shape():
    df = pd.DataFrame({
            "age": [30],
            "years_employed": [2],
            "annual_income": [50000],
            "credit_score": [700],
            "credit_history_years": [5],
            "savings_assets": [10000],
            "current_debt": [2000],
            "defaults_on_file": [0],
            "delinquencies_last_2yrs": [0],
            "derogatory_marks": [0],
            "loan_amount": [5000],
            "interest_rate": [9.5],
            "occupation_status": ["Salaried"],
            "loan_intent": ["Education"],
            "product_type": ["Personal Loan"]
        })


    df = engineer_features(df)
    pre = create_preprocessor()
    out = pre.fit_transform(df)
    # resulting shape should have numeric cols + onehot columns
    assert out.shape[0] == 1