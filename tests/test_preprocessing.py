from pathlib import Path

import pandas as pd
import pytest

try:
    import sklearn.model_selection  # noqa: F401
except ImportError as exc:
    pytest.skip(f"scikit-learn model_selection unavailable: {exc}", allow_module_level=True)

from src.preprocessing.pipeline import PreprocessConfig, build_train_test_sets


def test_preprocessing_outputs_expected_files(tmp_path):
    frame = pd.read_csv(Path("data/sample/sample_cicids_like.csv"))
    metadata = build_train_test_sets(
        frame,
        tmp_path,
        PreprocessConfig(test_size=0.25, max_features=10, random_state=7),
    )

    assert (tmp_path / "X_train.csv").exists()
    assert (tmp_path / "X_test.csv").exists()
    assert (tmp_path / "preprocessing_metadata.json").exists()
    assert metadata["label_mapping"] == {"NORMAL": 0, "ATTACK": 1}
    assert len(metadata["selected_features"]) <= 10
