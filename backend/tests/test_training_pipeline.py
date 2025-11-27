import os
from src.train import train


def test_train_creates_model(tmp_path, monkeypatch):
    # run training (conftest monkeypatches train.load_data to use sample csv)
    train(save_artifacts=True)
    assert os.path.exists("models/loan_model.pkl")