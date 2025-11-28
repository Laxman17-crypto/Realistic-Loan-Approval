import os

# -----------------------------
# Project Directory Structure
# -----------------------------

project_structure = {
    "loan-approval-mlops": {
        "data": {
            "raw": {},
            "processed": {}
        },
        "notebooks": {
            "01_eda.ipynb": "",
            "02_feature_engineering.ipynb": "",
            "03_model_training.ipynb": ""
        },
        "src": {
            "data_preprocessing.py": "",
            "train.py": "",
            "predict.py": "",
            "schemas": {
                "input_schema.py": ""
            }
        },
        "models": {
            "model.pkl": "",
            "scaler.pkl": "",
            "encoder.pkl": ""
        },
        "api": {
            "main.py": ""
        },
        "tests": {},
        "requirements.txt": "",
        "Dockerfile": "",
        "README.md": ""
    }
}


# ----------------------------------------------------
# Function to generate folders and files recursively
# ----------------------------------------------------
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        # If content is a dict → create folder
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)

        # If content is a string → create file
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


# ----------------------------------------------------
# Main: Create Project
# ----------------------------------------------------
if __name__ == "__main__":
    base = os.getcwd()   # creates project in current directory
    create_structure(base, project_structure)
    print("🎉 Project template created successfully!")