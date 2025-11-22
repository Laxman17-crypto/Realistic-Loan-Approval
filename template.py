import os
from pathlib import Path

project_name = "src"

list_of_files = [

    # root python files
    "app.py",
    "predict.py",
    "requirements.txt",
    "Dockerfile",
    ".dockerignore",
    "demo.py",
    "setup.py",
    "pyproject.toml",
    "README.md",

    # data folder
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",

    # notebooks
    "notebooks/01_exploration.ipynb",
    "notebooks/02_feature_engineering.ipynb",
    "notebooks/03_model_training.ipynb",

    # config files
    "config/model.yaml",
    "config/schema.yaml",
    "config/aws.yaml",
    "config/mongo.yaml",
    "config/mlflow.yaml",

    # main package
    f"{project_name}/__init__.py",

    # components
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",  
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/components/model_pusher.py",

    # configuration / connectors
    f"{project_name}/configuration/__init__.py",
    f"{project_name}/configuration/mongo_connection.py",
    f"{project_name}/configuration/aws_connection.py",
    f"{project_name}/configuration/s3_syncer.py",

    # cloud storage
    f"{project_name}/cloud_storage/__init__.py",
    f"{project_name}/cloud_storage/aws_storage.py",

    # data access
    f"{project_name}/data_access/__init__.py",
    f"{project_name}/data_access/loan_data.py",

    # constants
    f"{project_name}/constants/__init__.py",
    f"{project_name}/constants/training_pipeline.py",

    # entities
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/entity/artifact_entity.py",
    f"{project_name}/entity/estimator.py",
    f"{project_name}/entity/s3_estimator.py",

    # exception & logging
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",

    # pipelines
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/pipeline/prediction_pipeline.py",

    # utilities
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",

    # tests (recommended)
    "tests/__init__.py",
    "tests/test_data_validation.py",
    "tests/test_data_transformation.py",
    "tests/test_model_training.py",
]

# create structure
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            # create empty file (you can write boilerplate later)
            pass
