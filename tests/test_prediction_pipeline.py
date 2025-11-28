from src.predict import predict_from_dict

def test_predict_from_dict_returns_expected_keys():
    sample = {
        "age": 30,
        "years_employed": 4,
        "annual_income": 50000,
        "credit_score": 700,
        "credit_history_years": 6,
        "savings_assets": 10000,
        "current_debt": 5000,
        "defaults_on_file": 0,
        "delinquencies_last_2yrs": 0,
        "derogatory_marks": 0,
        "loan_amount": 10000,
        "interest_rate": 10.5,
        "occupation_status": "Salaried",
        "loan_intent": "Education",
        "product_type": "Personal Loan"
    }

    res = predict_from_dict(sample)
    assert "prediction" in res
    assert "probability" in res