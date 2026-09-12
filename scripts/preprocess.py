from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.loader import load_cicids_csvs
from src.preprocessing.pipeline import PreprocessConfig, build_train_test_sets
from src.utils.paths import project_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preprocess CIC-IDS2017 CSV files.")
    parser.add_argument("--raw-dir", default="data/raw", help="Directory containing CIC-IDS2017 CSV files.")
    parser.add_argument("--output-dir", default="data/processed", help="Directory for processed train/test files.")
    parser.add_argument("--sample", action="store_true", help="Use the small sample dataset.")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--max-features", type=int, default=35)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frame = load_cicids_csvs(
        raw_dir=project_path(args.raw_dir),
        sample_path=project_path("data/sample/sample_cicids_like.csv"),
        use_sample=args.sample,
    )
    metadata = build_train_test_sets(
        frame,
        project_path(args.output_dir),
        PreprocessConfig(
            test_size=args.test_size,
            random_state=args.random_state,
            max_features=args.max_features,
        ),
    )
    print("Preprocessing completed.")
    print(f"Train rows: {metadata['train_rows']}")
    print(f"Test rows: {metadata['test_rows']}")
    print(f"Selected features: {len(metadata['selected_features'])}")


if __name__ == "__main__":
    main()
