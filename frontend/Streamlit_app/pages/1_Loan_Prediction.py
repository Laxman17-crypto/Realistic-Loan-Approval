import streamlit as st
import requests
import os

st.markdown("""
<div class="navbar"><h1>🔮 Loan Approval Prediction</h1></div>
""", unsafe_allow_html=True)

st.write("Fill the form and get prediction from **FastAPI backend**.")

API_URL = os.getenv("API_URL") + "/predict"

with st.form("prediction_form"):

    age = st.number_input("Age", 18, 100)
    years_employed = st.number_input("Years Employed", 0.0)
    annual_income = st.number_input("Annual Income", 0.0)
    credit_score = st.number_input("Credit Score", 300, 850)
    credit_history_years = st.number_input("Credit History (Years)", 0.0)
    savings_assets = st.number_input("Savings Amount", 0.0)
    current_debt = st.number_input("Current Debt", 0.0)

    interest_rate = st.number_input("Loan Interest Rate", 0.0)
    loan_amount = st.number_input("Loan Amount", 0.0)

    occupation_status = st.selectbox("Occupation Status", ["Salaried", "Self-Employed", "Student"])
    loan_intent = st.selectbox("Loan Intent", ["Education", "Debt Consolidation", "Medical", "Home Improvement"])
    product_type = st.selectbox("Product Type", ["Personal Loan", "Line of Credit"])

    submitted = st.form_submit_button("Predict Approval")

if submitted:
    data = {
        "age": age,
        "years_employed": years_employed,
        "annual_income": annual_income,
        "credit_score": credit_score,
        "credit_history_years": credit_history_years,
        "savings_assets": savings_assets,
        "current_debt": current_debt,
        "defaults_on_file": 0,
        "delinquencies_last_2yrs": 0,
        "derogatory_marks": 0,
        "loan_amount": loan_amount,
        "interest_rate": interest_rate,
        "occupation_status": occupation_status,
        "loan_intent": loan_intent,
        "product_type": product_type
    }

    with st.spinner("Calling API..."):
        try:
            response = requests.post(API_URL, json=data)

            if response.status_code != 200:
                st.error("❌ API Error")
                st.write("Response:", response.text)
            else:
                result = response.json()

                # FIXED CHECK
                if "result" not in result or "prediction" not in result["result"]:
                    st.error("❌ API did not return a prediction.")
                    st.write("API Response:", result)

                else:
                    output = result["result"]
                    prediction = output["prediction"]
                    probability = output["probability"]

                    st.markdown("### 📊 Prediction Result")

                    if prediction == 1:
                        st.success("✅ **Loan Approved**")
                        st.info(f"Approval Probability: **{probability*100:.2f}%**")
                    else:
                        st.error("❌ **Loan Not Approved**")
                        st.warning(f"Approval Probability: **{probability*100:.2f}%**")

        except Exception as e:
            st.error(f"🚨 API Connection Failed: {e}")
