import pandas as pd
import os
import pytest
import joblib

# small synthetic dataset for tests
SAMPLE_DF = pd.DataFrame([
    {
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
        "product_type": "Personal Loan",
        "loan_status": 1
    },
    {
        "age": 45,
        "years_employed": 12,
        "annual_income": 120000,
        "credit_score": 760,
        "credit_history_years": 15,
        "savings_assets": 40000,
        "current_debt": 10000,
        "defaults_on_file": 0,
        "delinquencies_last_2yrs": 1,
        "derogatory_marks": 0,
        "loan_amount": 20000,
        "interest_rate": 8.0,
        "occupation_status": "Self-Employed",
        "loan_intent": "Home Improvement",
        "product_type": "Line of Credit",
        "loan_status": 1
    }
])

@pytest.fixture(scope="session")
def sample_df(tmp_path_factory):
    """Create a small CSV file for tests and return its path."""
    tmpdir = tmp_path_factory.mktemp("data")
    path = tmpdir / "test_loan_data.csv"
    SAMPLE_DF.to_csv(path, index=False)
    return str(path)

@pytest.fixture(autouse=True)
def ensure_models_dir(tmp_path, monkeypatch, sample_df):
    """Ensure models directory exists and monkeypatch default data path in train.load_data.


    This fixture runs automatically in tests to avoid touching your real data or models.
    """
    # ensure models folder exists in tmp test dir
    models_dir = tmp_path / "models"
    models_dir.mkdir()    
    
    # monkeypatch the working models path in modules that use 'models/..'
    monkeypatch.setenv("MODELS_DIR", str(models_dir))
    
    # monkeypatch src.train.load_data to read our sample csv instead of real dataset
    import src.train as train_mod
    
    def _load_data_patch(path=str(sample_df)):
        return pd.read_csv(path)
    
    monkeypatch.setattr(train_mod, "load_data", lambda path=None: _load_data_patch(path))


    yield
    
    for f in models_dir.glob("*"):
        try:
            f.unlink()
        except Exception:
            pass    