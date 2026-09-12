from __future__ import annotations

import time
from pathlib import Path

import joblib
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def should_enable_mlp_early_stopping(
    y_train: pd.Series,
    validation_fraction: float = 0.1,
) -> tuple[bool, str | None]:
    n_samples = len(y_train)
    n_classes = y_train.nunique()
    validation_size = int(n_samples * validation_fraction)
    if n_samples * validation_fraction > validation_size:
        validation_size += 1

    if validation_size < n_classes:
        message = (
            "MLP internal validation disabled: the training set is too small "
            f"for stratified validation ({n_samples} samples, {n_classes} classes, "
            f"validation_fraction={validation_fraction} would create only "
            f"{validation_size} validation sample(s)). This fallback is intended "
            "for tiny sample datasets; larger datasets keep internal validation enabled."
        )
        return False, message

    if y_train.value_counts().min() < 2:
        message = (
            "MLP internal validation disabled: at least one class has fewer than "
            "2 training samples, so stratified internal validation is not possible. "
            "This fallback is intended for tiny sample datasets; larger datasets "
            "keep internal validation enabled."
        )
        return False, message

    return True, None


def build_model(model_name: str, random_state: int = 42, y_train: pd.Series | None = None) -> Pipeline:
    if model_name == "random_forest":
        from sklearn.ensemble import RandomForestClassifier

        classifier = RandomForestClassifier(
            n_estimators=200,
            class_weight="balanced",
            random_state=random_state,
            n_jobs=-1,
        )
        return Pipeline([("imputer", SimpleImputer(strategy="median")), ("classifier", classifier)])

    if model_name == "svm":
        from sklearn.svm import SVC

        classifier = SVC(
            kernel="rbf",
            C=1.0,
            gamma="scale",
            class_weight="balanced",
            probability=True,
            random_state=random_state,
        )
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("classifier", classifier),
            ]
        )

    if model_name == "neural_network":
        from sklearn.neural_network import MLPClassifier

        validation_fraction = 0.1
        early_stopping = True
        if y_train is not None:
            early_stopping, message = should_enable_mlp_early_stopping(
                y_train,
                validation_fraction=validation_fraction,
            )
            if message:
                print(message)

        classifier = MLPClassifier(
            hidden_layer_sizes=(64, 32),
            max_iter=300,
            early_stopping=early_stopping,
            validation_fraction=validation_fraction,
            random_state=random_state,
        )
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("classifier", classifier),
            ]
        )

    raise ValueError(f"Unsupported model '{model_name}'.")


def train_and_save_model(
    model_name: str,
    x_train: pd.DataFrame,
    y_train: pd.Series,
    models_dir: Path,
    random_state: int = 42,
) -> dict[str, object]:
    model = build_model(model_name, random_state=random_state, y_train=y_train)

    x_fit = x_train
    y_fit = y_train

    if model_name == "svm" and len(x_train) > 5_000:
        from sklearn.model_selection import train_test_split

        x_fit, _, y_fit, _ = train_test_split(
            x_train,
            y_train,
            train_size=5_000,
            stratify=y_train,
            random_state=random_state,
        )
        print(
            f"SVM training subset: {len(x_fit):,} samples "
            f"(stratified from {len(x_train):,} training samples)."
        )

    start = time.perf_counter()
    model.fit(x_fit, y_fit)
    training_time = time.perf_counter() - start

    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / f"{model_name}.joblib"
    joblib.dump(model, model_path)
    return {"model_name": model_name, "model_path": str(model_path), "training_time_seconds": training_time}


def load_model(model_path: Path):
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")
    return joblib.load(model_path)
