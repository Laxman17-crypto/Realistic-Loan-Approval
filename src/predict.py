import joblib
import pandas as pd
from data_preprocessing import engineer_features
from utils.logger import logger
from utils.exception import CustomException


MODEL_PATH = "models/loan_model.pkl"
_pipeline = None


def load_pipeline():
    global _pipeline
    try:
        if _pipeline is None:
            _pipeline = joblib.load(MODEL_PATH)
            logger.info("Loaded prediction pipeline.")
        return _pipeline
    except Exception as e:
        raise CustomException(e)


def predict_from_dict(payload: dict):
    try:
        pipeline = load_pipeline()
        df = pd.DataFrame([payload])
        logger.info("Payload received for prediction.")
        df = engineer_features(df)
        logger.info("Features engineered for prediction.")
        preds = pipeline.predict(df)
        result = {"prediction": int(preds[0])}
        try:
            prob = pipeline.predict_proba(df)[0, 1]
            result["probability"] = float(prob)
        except:
            result["probability"] = None

        return result
    except Exception as e:
        raise CustomException(e)

