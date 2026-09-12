from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.ids.predictor import align_features
from src.models.trainers import load_model
from src.utils.io import load_json


st.set_page_config(page_title="Intelligent Network IDS", layout="wide")
st.title("Intelligent Network Intrusion Detection System")

models = sorted((PROJECT_ROOT / "models").glob("*.joblib"))
metadata_path = PROJECT_ROOT / "data/processed/preprocessing_metadata.json"

if not metadata_path.exists():
    st.warning("Run preprocessing first. Results will be generated after running the training pipeline.")
    st.stop()

metadata = load_json(metadata_path)
selected_features = metadata["selected_features"]

left, right = st.columns([1, 1])

with left:
    st.subheader("Prediction")
    if not models:
        st.info("No trained model found. Train at least one model before prediction.")
    model_path = st.selectbox("Model", models, format_func=lambda path: path.stem) if models else None
    uploaded = st.file_uploader("Flow features CSV or JSON", type=["csv", "json"])

    manual_values = {}
    with st.expander("Manual feature input"):
        for feature in selected_features:
            manual_values[feature] = st.number_input(feature, value=0.0)

    if st.button("Predict", disabled=model_path is None):
        model = load_model(model_path)
        if uploaded:
            if uploaded.name.endswith(".csv"):
                frame = pd.read_csv(uploaded)
            else:
                payload = json.loads(uploaded.read().decode("utf-8"))
                frame = pd.DataFrame([payload] if isinstance(payload, dict) else payload)
        else:
            frame = pd.DataFrame([manual_values])
        aligned = align_features(frame, metadata_path)
        predictions = model.predict(aligned)

        probabilities = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(aligned)

        results = []
        for index, prediction in enumerate(predictions, start=1):
            label = "ATTACK" if int(prediction) == 1 else "NORMAL"
            confidence = None

            if probabilities is not None:
                confidence = float(max(probabilities[index - 1]))

            results.append(
                {
                    "Flow": index,
                    "Prediction": label,
                    "Confidence": "N/A" if confidence is None else f"{confidence:.2%}",
                }
            )

        results_frame = pd.DataFrame(results)

        st.dataframe(
            results_frame,
            use_container_width=True,
            hide_index=True,
        )

        attack_count = int((predictions == 1).sum())
        normal_count = int((predictions == 0).sum())

        metric_left, metric_right = st.columns(2)

        metric_left.metric("NORMAL flows", normal_count)
        metric_right.metric("ATTACK flows", attack_count)

with right:
    st.subheader("Metrics")
    comparison_path = PROJECT_ROOT / "results/metrics/model_comparison.csv"
    if comparison_path.exists():
        st.dataframe(pd.read_csv(comparison_path), use_container_width=True)
    else:
        st.info("Results will be generated after running the training pipeline.")

    figures = sorted((PROJECT_ROOT / "results/figures").glob("*.png"))
    if figures:
        selected_figure = st.selectbox("Figure", figures, format_func=lambda path: path.name)
        st.image(str(selected_figure), use_container_width=True)

st.subheader("Dataset Status")
raw_files = sorted((PROJECT_ROOT / "data/raw").glob("*.csv"))
st.write(f"Raw CIC-IDS2017 CSV files detected: {len(raw_files)}")
st.write(f"Selected features: {len(selected_features)}")
