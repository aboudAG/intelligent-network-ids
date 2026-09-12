from pathlib import Path

import pandas as pd
import pytest

try:
    import sklearn.ensemble  # noqa: F401
except ImportError as exc:
    pytest.skip(f"scikit-learn native module unavailable: {exc}", allow_module_level=True)

from src.ids.predictor import predict
from src.models.trainers import train_and_save_model
from src.preprocessing.pipeline import PreprocessConfig, build_train_test_sets, load_processed_dataset


def test_mlp_trains_on_tiny_sample_dataset(tmp_path):
    frame = pd.read_csv(Path("data/sample/sample_cicids_like.csv"))
    processed_dir = tmp_path / "processed"
    models_dir = tmp_path / "models"
    build_train_test_sets(frame, processed_dir, PreprocessConfig(test_size=0.25, max_features=8))
    x_train, _, y_train, _ = load_processed_dataset(processed_dir)

    summary = train_and_save_model("neural_network", x_train, y_train, models_dir)

    assert Path(summary["model_path"]).exists()


def test_prediction_format_after_minimal_training(tmp_path):
    frame = pd.read_csv(Path("data/sample/sample_cicids_like.csv"))
    processed_dir = tmp_path / "processed"
    models_dir = tmp_path / "models"
    build_train_test_sets(frame, processed_dir, PreprocessConfig(test_size=0.25, max_features=8))
    x_train, _, y_train, _ = load_processed_dataset(processed_dir)
    train_and_save_model("random_forest", x_train, y_train, models_dir)

    results = predict(
        models_dir / "random_forest.joblib",
        Path("data/sample/sample_cicids_like.csv"),
        processed_dir / "preprocessing_metadata.json",
    )

    assert results
    assert results[0]["prediction"] in {"NORMAL", "ATTACK"}
    assert results[0]["confidence"] is None or 0 <= results[0]["confidence"] <= 1
