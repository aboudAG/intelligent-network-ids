from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.models.trainers import train_and_save_model
from src.preprocessing.pipeline import load_processed_dataset
from src.utils.io import load_json, save_json
from src.utils.paths import project_path


AVAILABLE_MODELS = ("random_forest", "svm", "neural_network")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train IDS machine learning models.")
    parser.add_argument("--processed-dir", default="data/processed")
    parser.add_argument("--models-dir", default="models")
    parser.add_argument("--model", choices=AVAILABLE_MODELS + ("all",), default="all")
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    x_train, _, y_train, _ = load_processed_dataset(project_path(args.processed_dir))
    selected_models = AVAILABLE_MODELS if args.model == "all" else (args.model,)
    training_summary_path = project_path("results/metrics/training_summary.json")

    if training_summary_path.exists():
        training_summary = load_json(training_summary_path)
    else:
        training_summary = {}

    for model_name in selected_models:
        summary = train_and_save_model(
            model_name,
            x_train,
            y_train,
            project_path(args.models_dir),
            random_state=args.random_state,
        )
        training_summary[model_name] = summary
        print(f"Trained {model_name}: {summary['model_path']}")

    save_json(training_summary, project_path("results/metrics/training_summary.json"))


if __name__ == "__main__":
    main()
