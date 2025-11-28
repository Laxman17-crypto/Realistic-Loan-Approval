from pydantic import BaseModel, Field

class LoanInput(BaseModel):
    age: int = Field(..., ge=18, le=100)
    years_employed: float = Field(..., ge=0)
    annual_income: float = Field(..., ge=0)
    credit_score: int = Field(..., ge=300, le=850)
    credit_history_years: float = Field(..., ge=0)
    savings_assets: float = Field(..., ge=0)
    current_debt: float = Field(..., ge=0)
    defaults_on_file: int = Field(..., ge=0)
    delinquencies_last_2yrs: int = Field(..., ge=0)
    derogatory_marks: int = Field(..., ge=0)
    loan_amount: float = Field(..., ge=0)
    interest_rate: float = Field(..., ge=0)
    occupation_status: str
    loan_intent: str
    product_type: str


class Config:
    schema_extra = {
        "example": {
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
    }