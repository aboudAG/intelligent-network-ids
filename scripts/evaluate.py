from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.metrics import evaluate_model, save_comparison_table, save_metrics
from src.models.trainers import load_model
from src.preprocessing.pipeline import load_processed_dataset
from src.utils.io import load_json
from src.utils.paths import project_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate trained IDS models.")
    parser.add_argument("--processed-dir", default="data/processed")
    parser.add_argument("--models-dir", default="models")
    parser.add_argument("--metrics-dir", default="results/metrics")
    parser.add_argument("--figures-dir", default="results/figures")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    _, x_test, _, y_test = load_processed_dataset(project_path(args.processed_dir))
    models_dir = project_path(args.models_dir)
    metrics_dir = project_path(args.metrics_dir)
    figures_dir = project_path(args.figures_dir)
    training_summary_path = metrics_dir / "training_summary.json"
    training_summary = load_json(training_summary_path) if training_summary_path.exists() else {}

    all_metrics = {}
    for model_path in sorted(models_dir.glob("*.joblib")):
        model_name = model_path.stem
        model = load_model(model_path)
        metrics = evaluate_model(model, x_test, y_test)
        metrics["training_time_seconds"] = training_summary.get(model_name, {}).get("training_time_seconds")
        save_metrics(model_name, metrics, metrics_dir, figures_dir)
        all_metrics[model_name] = metrics
        print(f"Evaluated {model_name}: F1={metrics['f1_score']:.4f}")

    if not all_metrics:
        raise FileNotFoundError(f"No trained .joblib models found in {models_dir}.")

    comparison = save_comparison_table(all_metrics, metrics_dir, figures_dir)
    print(f"Saved comparison table with {len(comparison)} model(s).")


if __name__ == "__main__":
    main()
