from pathlib import Path

from src.data.loader import load_cicids_csvs


def test_load_sample_dataset():
    frame = load_cicids_csvs(
        raw_dir=Path("data/raw"),
        sample_path=Path("data/sample/sample_cicids_like.csv"),
        use_sample=True,
    )
    assert not frame.empty
    assert "Label" in frame.columns
