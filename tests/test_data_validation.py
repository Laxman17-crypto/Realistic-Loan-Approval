from pydantic import ValidationError
from src.schemas.input_schema import LoanInput
import pytest

def test_valid_schema_example():
    example = LoanInput(
        age=30,
        years_employed=4,
        annual_income=50000,
        credit_score=700,
        credit_history_years=6,
        savings_assets=10000,
        current_debt=5000,
        defaults_on_file=0,
        delinquencies_last_2yrs=0,
        derogatory_marks=0,
        loan_amount=10000,
        interest_rate=10.5,
        occupation_status="Salaried",
        loan_intent="Education",
        product_type="Personal Loan"
    )
    assert example.age == 30
    
def test_schema_missing_field():
    with pytest.raises(ValidationError):
        LoanInput(
            # missing required field: annual_income
            age=30,
            years_employed=4,
            credit_score=700,
            credit_history_years=6,
            savings_assets=10000,
            current_debt=5000,
            defaults_on_file=0,
            delinquencies_last_2yrs=0,
            derogatory_marks=0,
            loan_amount=10000,
            interest_rate=10.5,
            occupation_status="Salaried",
            loan_intent="Education",
            product_type="Personal Loan"
        )
        
def test_schema_bad_values():
    with pytest.raises(ValidationError):
        LoanInput(
            age=15, # too young
            years_employed=4,
            annual_income=50000,
            credit_score=700,
            credit_history_years=6,
            savings_assets=10000,
            current_debt=5000,
            defaults_on_file=0,
            delinquencies_last_2yrs=0,
            derogatory_marks=0,
            loan_amount=10000,
            interest_rate=10.5,
            occupation_status="Salaried",
            loan_intent="Education",
            product_type="Personal Loan"
        )            