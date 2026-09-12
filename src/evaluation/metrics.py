from __future__ import annotations

import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from src.utils.io import save_json


def false_positive_rate(y_true, y_pred) -> float:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    denominator = fp + tn
    return float(fp / denominator) if denominator else 0.0


def evaluate_model(model, x_test: pd.DataFrame, y_test: pd.Series) -> dict[str, object]:
    start = time.perf_counter()
    y_pred = model.predict(x_test)
    prediction_time = time.perf_counter() - start

    return {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
        "false_positive_rate": false_positive_rate(y_test, y_pred),
        "prediction_time_seconds": prediction_time,
        "confusion_matrix": confusion_matrix(y_test, y_pred, labels=[0, 1]).tolist(),
        "classification_report": classification_report(
            y_test,
            y_pred,
            labels=[0, 1],
            target_names=["NORMAL", "ATTACK"],
            zero_division=0,
            output_dict=True,
        ),
    }


def save_confusion_matrix_figure(matrix: list[list[int]], title: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(5, 4))
    sns.heatmap(
        matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["NORMAL", "ATTACK"],
        yticklabels=["NORMAL", "ATTACK"],
    )
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def save_metrics(model_name: str, metrics: dict[str, object], metrics_dir: Path, figures_dir: Path) -> None:
    save_json(metrics, metrics_dir / f"{model_name}_metrics.json")
    save_confusion_matrix_figure(
        metrics["confusion_matrix"],
        f"{model_name} confusion matrix",
        figures_dir / f"{model_name}_confusion_matrix.png",
    )


def save_comparison_table(all_metrics: dict[str, dict[str, object]], metrics_dir: Path, figures_dir: Path) -> pd.DataFrame:
    rows = []
    for model_name, metrics in all_metrics.items():
        rows.append(
            {
                "model": model_name,
                "accuracy": metrics["accuracy"],
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1_score": metrics["f1_score"],
                "false_positive_rate": metrics["false_positive_rate"],
                "prediction_time_seconds": metrics["prediction_time_seconds"],
                "training_time_seconds": metrics.get("training_time_seconds"),
            }
        )

    comparison = pd.DataFrame(rows).sort_values("model")
    metrics_dir.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(metrics_dir / "model_comparison.csv", index=False)

    for metric in ["accuracy", "precision", "recall", "f1_score", "false_positive_rate"]:
        plt.figure(figsize=(7, 4))
        sns.barplot(data=comparison, x="model", y=metric)
        plt.ylim(0, 1)
        plt.title(f"Model comparison - {metric}")
        plt.tight_layout()
        figures_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(figures_dir / f"comparison_{metric}.png", dpi=160)
        plt.close()

    return comparison
