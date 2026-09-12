# Intelligent Network Intrusion Detection System (ML-based IDS)

Prototype de détection d'intrusions réseau basé sur le Machine Learning. Le
projet suit le sujet universitaire présent dans le PDF
`Sujet_1_TER___Master_RSA-Securité-5_3a1ecab9af460c8a7ffed5880901dc2a.pdf`,
situé dans le dossier `Downloads`.

## Context

Un IDS analyse le trafic réseau pour détecter des comportements suspects. Ce
projet construit une chaîne complète autour de CIC-IDS2017 pour classifier des
flux réseau en deux classes :

- `NORMAL`
- `ATTACK`

Results will be generated after running the training pipeline.

## Objectives

- Charger et préparer des fichiers CSV CIC-IDS2017.
- Nettoyer les données, encoder les labels et sélectionner des features.
- Entraîner Random Forest, SVM et un réseau de neurones simple.
- Évaluer les modèles avec accuracy, precision, recall, F1-score et false
  positive rate.
- Générer des matrices de confusion et des figures comparatives.
- Fournir une commande de prédiction et un dashboard Streamlit local.
- Garder une architecture évolutive vers une détection quasi temps réel.

## Architecture

```text
Network Traffic / Dataset
        |
Data preprocessing
        |
Feature engineering / feature selection
        |
Train / Validation / Test
        |
Machine Learning models
        |
Prediction
        |
Evaluation
        |
IDS detection
        |
Dashboard / visualization
```

## Technologies

- Python
- pandas, NumPy
- scikit-learn
- joblib
- matplotlib, seaborn
- Streamlit
- pytest

## Dataset

Dataset principal : CIC-IDS2017.

Téléchargement officiel : page CIC-IDS2017 de l'Institut canadien de
cybersécurité, University of New Brunswick:
`https://www.unb.ca/cic/datasets/ids-2017.html`

Ne placez pas le dataset complet dans Git. Copiez les CSV dans :

```text
data/raw/
```

Fichiers typiques :

- `Monday-WorkingHours.pcap_ISCX.csv`
- `Tuesday-WorkingHours.pcap_ISCX.csv`
- `Wednesday-workingHours.pcap_ISCX.csv`
- `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv`
- `Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv`
- `Friday-WorkingHours-Morning.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`

Un petit fichier `data/sample/sample_cicids_like.csv` est fourni pour tester le
pipeline sans télécharger CIC-IDS2017.

## Project Structure

```text
Intelligent-Network-IDS/
├── README.md
├── LICENSE
├── requirements.txt
├── config/
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
├── src/
│   ├── data/
│   ├── preprocessing/
│   ├── models/
│   ├── evaluation/
│   ├── ids/
│   └── utils/
├── scripts/
├── dashboard/
├── docs/
├── models/
├── results/
│   ├── figures/
│   ├── metrics/
│   └── reports/
├── notebooks/
└── tests/
```

## Installation

Depuis le dossier du projet :

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Sur Linux/macOS :

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Preprocessing

Avec CIC-IDS2017 placé dans `data/raw/` :

```bash
python scripts/preprocess.py
```

Sans CIC-IDS2017, pour tester avec le fichier d'exemple :

```bash
python scripts/preprocess.py --sample
```

Le script génère :

- `data/processed/X_train.csv`
- `data/processed/X_test.csv`
- `data/processed/y_train.csv`
- `data/processed/y_test.csv`
- `data/processed/preprocessing_metadata.json`

## Training

Entraîner les trois modèles :

```bash
python scripts/train.py --model all
```

Entraîner un seul modèle :

```bash
python scripts/train.py --model random_forest
python scripts/train.py --model svm
python scripts/train.py --model neural_network
```

Les modèles sont sauvegardés dans `models/` au format `.joblib`.

## Evaluation

```bash
python scripts/evaluate.py
```

Métriques générées :

- accuracy
- precision
- recall
- F1-score
- false positive rate
- confusion matrix
- classification report
- prediction time
- training time lorsque disponible

Les résultats sont sauvegardés dans :

- `results/metrics/`
- `results/figures/`

Le tableau de comparaison est exporté ici :

```text
results/metrics/model_comparison.csv
```

## Prediction

Après preprocessing et entraînement :

```bash
python scripts/predict.py --model models/random_forest.joblib --input data/sample/sample_cicids_like.csv
```

Sortie attendue :

```text
Prediction: ATTACK
Confidence: 93.20%
```

La confiance dépend du modèle utilisé et des données.

## Quasi Real-Time Prototype

Le projet inclut un prototype de détection quasi temps réel basé sur des dépôts
de CSV. Il ne capture pas encore de trafic réseau réel.

```bash
python scripts/realtime_csv_watch.py --input-dir data/live --model models/random_forest.joblib
```

Ce qui est réellement implémenté :

- surveillance d'un dossier local ;
- prédiction sur chaque nouveau fichier CSV ;
- réutilisation du même preprocessing que l'entraînement.

Ce qui est une perspective :

- capture PCAP réelle ;
- extraction automatique de flows via CICFlowMeter, Zeek ou un collecteur réseau ;
- intégration SIEM ou alerting.

## Dashboard

```bash
streamlit run dashboard/app.py
```

Le dashboard permet de :

- sélectionner un modèle entraîné ;
- fournir des caractéristiques de trafic via fichier ou saisie manuelle ;
- obtenir une prédiction `NORMAL` ou `ATTACK` ;
- afficher les métriques disponibles ;
- visualiser les figures générées.

## Results

Aucun résultat expérimental n'est inventé dans ce dépôt.

Results will be generated after running the training pipeline.

Après exécution sur CIC-IDS2017, utilisez :

- `results/metrics/model_comparison.csv`
- `results/figures/*`
- `results/metrics/*_metrics.json`

Interprétez le meilleur modèle à partir des métriques réelles. En cybersécurité,
un très bon score d'accuracy peut masquer un taux de faux positifs ou de faux
négatifs problématique. Comparez donc precision, recall, F1-score et false
positive rate.

## Tests

```bash
pytest
```

Les tests couvrent le chargement des données d'exemple, le preprocessing et le
format d'une prédiction après entraînement minimal.

Vérification de l'environnement :

```bash
python scripts/check_environment.py
```

Sur Windows, si un message indique qu'une stratégie de contrôle d'application
bloque un fichier `.dll` ou `.pyd`, essayez depuis la racine du projet :

```powershell
Get-ChildItem -LiteralPath .\.venv -Recurse -File | Unblock-File
```

## Skills Demonstrated

- Network Security
- Intrusion Detection
- Machine Learning
- Python
- Data preprocessing
- Network traffic analysis
- Security analytics

## Limitations

- Le projet est un prototype ML sur features de flux, pas un IDS de production.
- La capture réseau réelle n'est pas encore implémentée.
- Les performances dépendent du nettoyage, des fichiers CIC-IDS2017 utilisés et
  de la distribution des classes.
- SVM peut être coûteux sur le dataset complet.

## Perspectives

- Ajouter une validation croisée contrôlée.
- Connecter CICFlowMeter ou Zeek pour extraire des flows depuis PCAP.
- Ajouter une API REST pour exposer la prédiction.
- Ajouter un système d'alerting.
- Étendre la classification binaire vers une classification multi-attaques.

## License

MIT License.
