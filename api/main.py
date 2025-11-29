# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.schemas.input_schema import LoanInput
from src.predict import predict_from_dict

app = FastAPI(title="Loan Approval Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict")
def predict(application: LoanInput):
    payload = application.model_dump()
    result = predict_from_dict(payload)
    return {"success": True, "result": result}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def home():
    return {'message':'Loan approval prediction API'}