from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.utils.io import save_json


BENIGN_VALUES = {"BENIGN", "NORMAL"}


@dataclass(frozen=True)
class PreprocessConfig:
    target_column: str = "Label"
    test_size: float = 0.2
    random_state: int = 42
    drop_columns: tuple[str, ...] = ("Flow ID", "Source IP", "Destination IP", "Timestamp")
    max_features: int | None = 35


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = {column: column.strip() for column in df.columns}
    return df.rename(columns=renamed)


def encode_binary_labels(series: pd.Series) -> pd.Series:
    labels = series.astype(str).str.strip().str.upper()
    return labels.apply(lambda value: 0 if value in BENIGN_VALUES else 1).astype(int)


def clean_dataframe(df: pd.DataFrame, config: PreprocessConfig) -> pd.DataFrame:
    df = normalize_columns(df)
    if config.target_column not in df.columns:
        raise ValueError(f"Target column '{config.target_column}' not found.")

    df = df.drop(columns=[col for col in config.drop_columns if col in df.columns], errors="ignore")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.drop_duplicates()
    df = df.dropna(subset=[config.target_column])

    for column in df.columns:
        if column != config.target_column:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    feature_columns = [column for column in df.columns if column != config.target_column]
    df[feature_columns] = df[feature_columns].replace([np.inf, -np.inf], np.nan)
    all_missing_features = [column for column in feature_columns if df[column].isna().all()]
    if all_missing_features:
        df = df.drop(columns=all_missing_features)
        feature_columns = [column for column in feature_columns if column not in all_missing_features]

    df = df.dropna(axis=0, how="all", subset=feature_columns)
    df[config.target_column] = encode_binary_labels(df[config.target_column])
    return df


def select_features_from_training(
    x_train: pd.DataFrame,
    max_features: int | None,
) -> list[str]:
    numeric_columns = list(x_train.select_dtypes(include=[np.number]).columns)
    if max_features is None or len(numeric_columns) <= max_features:
        return numeric_columns

    variances = x_train[numeric_columns].var(numeric_only=True).sort_values(ascending=False)
    return list(variances.head(max_features).index)


def build_train_test_sets(
    df: pd.DataFrame,
    output_dir: Path,
    config: PreprocessConfig,
) -> dict[str, object]:
    cleaned = clean_dataframe(df, config)
    y = cleaned[config.target_column]
    x = cleaned.drop(columns=[config.target_column])

    stratify = y if y.nunique() > 1 and y.value_counts().min() >= 2 else None
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=config.test_size,
        random_state=config.random_state,
        stratify=stratify,
    )

    selected_features = select_features_from_training(x_train, config.max_features)
    x_train = x_train[selected_features]
    x_test = x_test[selected_features]

    output_dir.mkdir(parents=True, exist_ok=True)
    x_train.to_csv(output_dir / "X_train.csv", index=False)
    x_test.to_csv(output_dir / "X_test.csv", index=False)
    y_train.to_csv(output_dir / "y_train.csv", index=False, header=[config.target_column])
    y_test.to_csv(output_dir / "y_test.csv", index=False, header=[config.target_column])

    metadata = {
        "target_column": config.target_column,
        "label_mapping": {"NORMAL": 0, "ATTACK": 1},
        "selected_features": selected_features,
        "test_size": config.test_size,
        "random_state": config.random_state,
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "class_distribution_train": {str(k): int(v) for k, v in y_train.value_counts().to_dict().items()},
        "class_distribution_test": {str(k): int(v) for k, v in y_test.value_counts().to_dict().items()},
    }
    save_json(metadata, output_dir / "preprocessing_metadata.json")
    return metadata


def load_processed_dataset(processed_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    x_train = pd.read_csv(processed_dir / "X_train.csv")
    x_test = pd.read_csv(processed_dir / "X_test.csv")
    y_train = pd.read_csv(processed_dir / "y_train.csv").iloc[:, 0]
    y_test = pd.read_csv(processed_dir / "y_test.csv").iloc[:, 0]
    return x_train, x_test, y_train, y_test
