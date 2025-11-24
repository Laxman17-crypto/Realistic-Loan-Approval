import os
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from data_preprocessing import create_preprocessor, engineer_features
from utils.logger import logger
from utils.exception import CustomException

MODEL_PATH = "models/loan_model.pkl"
PREPROCESSOR_PATH = "models/preprocessor.joblib"




def load_data(path="data/raw/Loan_approval_data_2025.csv"):
    df = pd.read_csv(path)
    # Drop any one-hot dummies if present in raw file
    dummy_prefixes = ["occupation_status_", "product_type_", "loan_intent_"]
    drop_cols = [c for c in df.columns if any(c.startswith(p) for p in dummy_prefixes)]
    df.drop('customer_id',axis=1,inplace=True)
    df = df.drop(columns=drop_cols, errors="ignore")
    return df




def train(save_artifacts: bool = True):
    try:
        os.makedirs("models", exist_ok=True)
        df = load_data()
        df = engineer_features(df)
        target = "loan_status"
        X = df.drop(columns=[target])
        y = df[target]


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        preprocessor = create_preprocessor()
    
        models = {
        "log_reg": LogisticRegression(max_iter=500),
        "random_forest": RandomForestClassifier(n_estimators=200, random_state=42),
        "xgboost": XGBClassifier(
                    eval_metric="logloss",
                    n_estimators=300,
                    learning_rate=0.05,
                    max_depth=5
            )
        } 

        best_model=None
        best_auc=-1

        for name, clf in models.items():
            logger.info(f"Training model: {name}")
            pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("clf", clf)
            ])

        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)


        try:
            prob = pipeline.predict_proba(X_test)[:,1]
            auc = roc_auc_score(y_test, prob)
        except:
            auc = 0


        logger.info(f"Model: {name} | AUC: {auc}")
        if auc > best_auc:
            best_auc = auc
            best_model = pipeline


        logger.info(f"Best model selected with AUC: {best_auc}")       

        pipeline = best_model([
                ("preprocessor", preprocessor),
                ("clf", clf)
            ])
        pipeline.fit(X_train, y_train)
        logger.info("Model training completed.")


        preds = pipeline.predict(X_test)
        logger.info("Evaluation:" + classification_report(y_test, preds))


        try:
            prob = pipeline.predict_proba(X_test)[:, 1]
            logger.info(f"ROC AUC: {roc_auc_score(y_test, prob)}")
        except:
            logger.warning("Model has no predict_proba method.")


        if save_artifacts:
            joblib.dump(pipeline, MODEL_PATH)
        logger.info(f"Saved trained pipeline to {MODEL_PATH}")


    except Exception as e:
        raise CustomException(e)




if __name__ == "__main__":
    train()