from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.ids.realtime import run_csv_watch
from src.utils.paths import project_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prototype quasi real-time IDS watcher for CSV flow drops.")
    parser.add_argument("--input-dir", default="data/live")
    parser.add_argument("--model", default="models/random_forest.joblib")
    parser.add_argument("--metadata", default="data/processed/preprocessing_metadata.json")
    parser.add_argument("--interval", type=float, default=2.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = project_path(args.input_dir)
    input_dir.mkdir(parents=True, exist_ok=True)
    print(f"Watching {input_dir} for CSV files. Press Ctrl+C to stop.")
    run_csv_watch(project_path(args.model), project_path(args.metadata), input_dir, args.interval)


if __name__ == "__main__":
    main()
