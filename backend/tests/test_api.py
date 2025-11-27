from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_api_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_api_predict_endpoint():
    payload = {
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

    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("success") is True
    assert "result" in body