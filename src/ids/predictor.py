from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.models.trainers import load_model
from src.utils.io import load_json


def load_input(input_path: Path) -> pd.DataFrame:
    if input_path.suffix.lower() == ".csv":
        return pd.read_csv(input_path)
    if input_path.suffix.lower() == ".json":
        payload = json.loads(input_path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            return pd.DataFrame([payload])
        return pd.DataFrame(payload)
    raise ValueError("Input must be a CSV or JSON file.")


def align_features(frame: pd.DataFrame, metadata_path: Path) -> pd.DataFrame:
    metadata = load_json(metadata_path)
    selected_features = metadata["selected_features"]
    aligned = frame.copy()
    aligned.columns = [column.strip() for column in aligned.columns]
    for feature in selected_features:
        if feature not in aligned.columns:
            aligned[feature] = None
    aligned = aligned[selected_features]
    for feature in selected_features:
        aligned[feature] = pd.to_numeric(aligned[feature], errors="coerce")
    return aligned.replace([np.inf, -np.inf], np.nan)


def predict(model_path: Path, input_path: Path, metadata_path: Path) -> list[dict[str, object]]:
    model = load_model(model_path)
    frame = align_features(load_input(input_path), metadata_path)
    predictions = model.predict(frame)

    probabilities = None
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(frame)

    results = []
    for index, prediction in enumerate(predictions):
        label = "ATTACK" if int(prediction) == 1 else "NORMAL"
        confidence = None
        if probabilities is not None:
            confidence = float(max(probabilities[index]))
        results.append({"prediction": label, "confidence": confidence})
    return results
