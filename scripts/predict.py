from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.ids.predictor import predict
from src.utils.paths import project_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predict NORMAL or ATTACK from network flow features.")
    parser.add_argument("--input", required=True, help="Input CSV or JSON file containing flow features.")
    parser.add_argument("--model", default="models/random_forest.joblib", help="Path to a trained model.")
    parser.add_argument(
        "--metadata",
        default="data/processed/preprocessing_metadata.json",
        help="Path to preprocessing metadata.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = predict(project_path(args.model), project_path(args.input), project_path(args.metadata))
    for index, result in enumerate(results, start=1):
        confidence = result["confidence"]
        confidence_text = "N/A" if confidence is None else f"{confidence:.2%}"
        print(f"Flow #{index}")
        print(f"Prediction: {result['prediction']}")
        print(f"Confidence: {confidence_text}")


if __name__ == "__main__":
    main()
