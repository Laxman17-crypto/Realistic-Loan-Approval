import streamlit as st

st.set_page_config(page_title="Loan Approval System", layout="wide")

# -----------------------------------
#            CUSTOM CSS
# -----------------------------------
st.markdown("""
<style>

:root {
    --primary: #4A90E2;
    --primary-light: #74aef3;
    --dark: #1f1f1f;
    --text: #1e1e1e;
    --light-bg: #f6f9ff;
    --card: rgba(255, 255, 255, 0.55);
}

/* Main App Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e6edff, #fdfdff, #eef6ff);
    font-family: 'Inter', sans-serif;
    color: var(--text);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(200,200,200,0.4);
}
[data-testid="stSidebar"] h1 {
    font-weight: 700;
    color: var(--primary);
}

/* Navbar Header */
.navbar {
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(15px);
    padding: 15px 25px;
    border-radius: 16px;
    margin-bottom: 25px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}
.navbar h1 {
    margin: 0;
    font-size: 32px;
    font-weight: 800;
    color: var(--primary);
}

/* KPI Cards */
.kpi-card {
    background: var(--card);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    backdrop-filter: blur(20px);
    transition: 0.3s;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.15);
}
.kpi-card h2 {
    font-size: 38px;
    margin-bottom: 8px;
    font-weight: 700;
    color: var(--primary);
}
.kpi-card p {
    font-size: 16px;
    font-weight: 600;
}

/* Glass Cards */
.glass-card {
    background: var(--card);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.05);
    backdrop-filter: blur(18px);
    margin-bottom: 25px;
    transition: 0.3s;
}
.glass-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 28px rgba(0,0,0,0.15);
}

/* Center Container */
.block-container {
    padding-top: 20px;
    max-width: 1100px;
    margin: auto;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
#         NAVBAR
# -----------------------------------
st.markdown("""
<div class="navbar">
    <h1>🏦 Loan Approval ML System</h1>
</div>
""", unsafe_allow_html=True)


# -----------------------------------
#      ABOUT ME SECTION
# -----------------------------------
st.subheader("👨‍💼 About Me")

st.markdown("""
### **🔹 Laxman Sahani**  
B.Tech in **Mechanical Engineering**  
**Jabalpur Engineering College (JEC), India**  

I am passionate about **Machine Learning, Data Science, MLOps**, and building real-world intelligent systems.  
This Loan Approval ML System demonstrates complete end-to-end ML engineering:

✔ Data Engineering  
✔ Feature Engineering  
✔ Modular ML Code  
✔ MLOps pipeline  
✔ REST API using FastAPI  
✔ Streamlit UI  
✔ Model Deployment Ready  
""")

st.markdown("---")

# -----------------------------------
#      DASHBOARD KPI CARDS
# -----------------------------------
st.subheader("📊 System Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="kpi-card">
        <h2>28</h2>
        <p>Engineered Features</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="kpi-card">
        <h2>3</h2>
        <p>Models Trained (LogReg / RF / XGB)</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="kpi-card">
        <h2>API</h2>
        <p>FastAPI Live Prediction</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.write("Use the sidebar to navigate → Prediction | EDA Dashboard")
