# 🚀 Realistic Loan Approval Prediction System
A **full-stack Machine Learning project** that predicts **loan approval eligibility** using a trained ML model served via FastAPI backend and a Streamlit UI frontend.
Everything is containerized with **Docker** and deployed on **Render Cloud**.

## ✨ Features

✔ ML model trained on real-world loan dataset

✔ FastAPI backend exposing /predict API

✔ Streamlit interactive UI frontend

✔ Docker containerization (frontend + backend)

✔ Live cloud deployment (Render)

✔ Environment-based configurable API URLs

✔ Supports categorical + numerical input

✔ Health check endpoint for monitoring

## 📌 Project Architecture
```
Frontend (Streamlit UI)
	↓ calls API
Backend (FastAPI)
	↓ loads ML model
Predictor → Returns JSON output
```

## 📂 Directory Structure
```
Realistic-Loan-Approval/
└── api
|   └── data
|       └── processed/loan_data_processed.csv
|       └── raw/Loan_approval_data_2025.csv/realistic-loan-approval-dataset-us-and-canada.zip
|   └── models
|       ├── encoder.pkl
|       ├── loan_model.pkl
|       ├── model.pkl
|       ├── scaler.pkl
|   └── src
|       └── schemas
|           ├── input_schema.py
|       └── utils
|           ├── exception.py
|           ├── logger.py
|       ├── data_preprocessing.py
|       ├── predict.py
|       ├── train.py
|    ├── main.py
|    └── requirements.txt
│
├── frontend/
│   ├── Streamlit_app/
│   │   ├── app.py
│   │   └── pages/1_Loan_Prediction.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── render.yaml
└── README.md
```
# ⚙️ Tech Stack

| Layer            | Technology                             |
| ---------------- | -------------------------------------- |
| Frontend UI      | Streamlit                              |
| API Backend      | FastAPI                                |
| Model Serving    | Pickled ML Model                       |
| ML Models Used   | CatBoost / RandomForest / XGBoost etc. |
| Deployment       | Render Cloud                           |
| Containerization | Docker & Docker Compose                |

## 🧠 Machine Learning Workflow
✔ Data preprocessing

✔ Feature encoding

✔ Train/test split

✔ Model training

✔ Probabilistic prediction

✔ Model persistence (model.pkl)

✔ API-based inference

## 🔥 Running Locally
### 1️⃣ Clone the Repository
```
git clone https://github.com/your-username/Realistic-Loan-Approval.git
cd Realistic-Loan-Approval
```
### 2️⃣ Start using Docker Compose
```
docker-compose up --build
```
This will start:

✔ api → http://localhost:8000

✔ Frontend → http://localhost:8501

## 🔗 API Documentation (Swagger)
FastAPI provides live docs:

➡ /docs

➡ /redoc

Example:(Note first deploy api and streamlit_app on render)
```
https://loan-backend.onrender.com/docs
```
if locally(Without deployment)
```
http://localhost:8000/docs
```
## 🔐 Environment Variables
Backend .env
```
MODEL_PATH=src/model.pkl
```
Frontend .env
```
API_URL=http://backend:8000
```
On Render, API_URL is added via Environment Variables UI.

## 📌 Future Enhancements

- Logging & Monitoring

- JWT authentication

- Database integration (MongoDB/PostgreSQL)

- Model retraining pipeline

- CI/CD automation

# 👨‍💻 Author
## Lucky / Laxman

🎯 ML Engineer | FastAPI | Streamlit | DevOps Learner

🔗 GitHub: https://github.com/Laxman17-crypto

## ⭐ Contribute

Feel free to fork, improve UI/ML and create a PR.

Star ⭐ the repo if you liked it!

