from __future__ import annotations

from pathlib import Path

import pandas as pd


CICIDS2017_CSV_FILENAMES = (
    "Monday-WorkingHours.pcap_ISCX.csv",
    "Tuesday-WorkingHours.pcap_ISCX.csv",
    "Wednesday-workingHours.pcap_ISCX.csv",
    "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
    "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
    "Friday-WorkingHours-Morning.pcap_ISCX.csv",
    "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
    "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
)


def find_csv_files(raw_dir: Path) -> list[Path]:
    return sorted(path for path in raw_dir.glob("*.csv") if path.is_file())


def read_cicids_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(
        path,
        low_memory=False,
        skipinitialspace=True,
        encoding_errors="replace",
    )


def load_cicids_csvs(raw_dir: Path, sample_path: Path | None = None, use_sample: bool = False) -> pd.DataFrame:
    if use_sample:
        if sample_path is None or not sample_path.exists():
            raise FileNotFoundError("Sample dataset not found.")
        return read_cicids_csv(sample_path)

    csv_files = find_csv_files(raw_dir)
    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {raw_dir}. Place CIC-IDS2017 CSV files there or use --sample."
        )

    print(f"Loading {len(csv_files)} CSV file(s) from {raw_dir}:")
    for path in csv_files:
        print(f"- {path.name}")

    frames = [read_cicids_csv(path) for path in csv_files]
    return pd.concat(frames, ignore_index=True)
