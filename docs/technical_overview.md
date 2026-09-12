# Technical Overview

## Traditional IDS

A traditional signature-based IDS compares network activity with known attack
patterns. It is effective for recognized threats and easy to explain, but it
can miss new attacks, variants, and behavior that does not match an existing
rule.

## Why Machine Learning

Machine learning can learn statistical patterns from network flow features.
For an IDS, this makes it possible to classify traffic as normal or suspicious
from attributes such as packet counts, byte counts, flow duration, flag counts,
and inter-arrival times. ML-based IDS approaches can complement signatures, but
they require careful data preparation and must be evaluated against false
positives.

## CIC-IDS2017 Usage

CIC-IDS2017 provides labeled network flow CSV files containing benign traffic
and several attack families. This project converts the original labels into a
binary task:

- `NORMAL`: benign traffic
- `ATTACK`: every non-benign label

The original dataset is not stored in this repository. Users place the CSV
files in `data/raw/`, then run the preprocessing script.

## Pipeline

1. Load one or more CSV files.
2. Normalize column names.
3. Drop identifier columns when present.
4. Replace infinite values with missing values.
5. Remove duplicates.
6. Encode labels as binary values.
7. Split into train and test sets.
8. Select features using training data only.
9. Train Random Forest, SVM, and MLP models.
10. Evaluate metrics and generate figures.
11. Use a saved model for IDS predictions.

Scaling and imputation are stored inside each scikit-learn pipeline. This keeps
training and inference consistent and avoids fitting preprocessing
transformations on the test set.

## Model Notes

Random Forest is often a strong baseline for tabular flow data. It handles
nonlinear relationships and usually needs less scaling.

SVM can perform well on smaller or medium-sized datasets but can be slower on
large CIC-IDS2017 files. This project uses probability estimates so prediction
confidence can be displayed.

The neural network is implemented as a simple MLP. It is intentionally modest
and easy to explain for an academic prototype. Larger architectures should only
be added after validating the baseline pipeline.

## Limitations

This is a flow-feature classifier, not a full packet capture IDS. It does not
extract flows from live traffic yet. The quasi real-time component currently
watches a directory for CSV flow files and applies a trained model to them.

Future work can connect a flow generator, PCAP parser, Zeek logs, CICFlowMeter,
or a live capture source to the same prediction interface.
