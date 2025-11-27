FROM python:3.10-slim

WORKDIR /app

# Copy requirements first
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit app folder
COPY Streamlit_app/ ./Streamlit_app/

EXPOSE 8501

CMD ["streamlit", "run", "Streamlit_app/app.py", "--server.address=0.0.0.0", "--server.port=8501"]