from __future__ import annotations

import time
from pathlib import Path
from typing import Iterator

from src.ids.predictor import predict


def poll_csv_directory(input_dir: Path, interval_seconds: float = 2.0) -> Iterator[Path]:
    """Prototype source adapter for quasi real-time IDS detection from CSV drops."""
    seen: set[Path] = set()
    while True:
        for path in sorted(input_dir.glob("*.csv")):
            if path not in seen:
                seen.add(path)
                yield path
        time.sleep(interval_seconds)


def run_csv_watch(model_path: Path, metadata_path: Path, input_dir: Path, interval_seconds: float = 2.0) -> None:
    for csv_path in poll_csv_directory(input_dir, interval_seconds=interval_seconds):
        for result in predict(model_path, csv_path, metadata_path):
            confidence = result["confidence"]
            confidence_text = "N/A" if confidence is None else f"{confidence:.2%}"
            print(f"{csv_path.name}: Prediction={result['prediction']} Confidence={confidence_text}")
