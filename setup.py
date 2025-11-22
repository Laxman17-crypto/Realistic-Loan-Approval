from setuptools import setup, find_packages

setup(
    name="loan_approval",
    version="0.1.0",
    description="Loan Approval Prediction ML Pipeline",
    author="Laxman Sahane",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "xgboost",
        "pyyaml",
        "python-dotenv",
        "joblib"
    ],
)
