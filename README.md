# Intelligent Network Intrusion Detection System

Système de détection d'intrusions réseau basé sur le Machine Learning et développé autour du dataset **CIC-IDS2017**.

L'objectif du projet est d'étudier la capacité de différents modèles de Machine Learning à distinguer automatiquement les flux réseau normaux des flux malveillants, puis de comparer leurs performances dans une configuration expérimentale reproductible.

---

## Présentation du projet

Un système de détection d'intrusions (IDS — Intrusion Detection System) analyse le trafic réseau afin d'identifier des comportements potentiellement malveillants.

Dans ce projet, une approche basée sur le Machine Learning est utilisée pour classifier les flux réseau en deux catégories :

- **NORMAL** : trafic considéré comme légitime
- **ATTACK** : trafic considéré comme malveillant

Le projet couvre l'ensemble de la chaîne expérimentale :

```text
                         CIC-IDS2017
                              │
                              ▼
                     Chargement des données
                              │
                              ▼
                    Nettoyage et prétraitement
                              │
                              ▼
                   Sélection des caractéristiques
                              │
                              ▼
                      Séparation Train / Test
                              │
                              ▼
                         Entraînement
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
          Random Forest      SVM      Neural Network
                │             │             │
                └─────────────┼─────────────┘
                              ▼
                         Évaluation
                              │
                              ▼
                    Comparaison des modèles
                              │
                              ▼
                      Couche de prédiction
                              │
                              ▼
                       Dashboard Streamlit
```

---

## Objectifs

Les principaux objectifs du projet sont :

- préparer et nettoyer un dataset de trafic réseau ;
- sélectionner les caractéristiques pertinentes pour la classification ;
- entraîner plusieurs modèles de Machine Learning ;
- comparer leurs performances ;
- analyser les erreurs de classification ;
- mesurer le taux de faux positifs ;
- utiliser les modèles entraînés pour classifier de nouveaux flux ;
- fournir une interface permettant de visualiser les prédictions.

---

## Dataset

Le projet utilise **CIC-IDS2017**, un dataset de trafic réseau contenant des flux normaux ainsi que différents scénarios d'attaques.

Dataset officiel :

https://www.unb.ca/cic/datasets/ids-2017.html

Les données complètes ne sont pas incluses dans ce dépôt GitHub afin d'éviter de versionner des fichiers volumineux.

### Structure des données

```text
data/
├── raw/
├── processed/
└── sample/
```

Un petit jeu de données de démonstration est fourni dans :

```text
data/sample/
```

Les fichiers complets du dataset doivent être placés dans :

```text
data/raw/
```

### Fichiers CIC-IDS2017 utilisés

Le pipeline attend les fichiers suivants :

```text
Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv
Friday-WorkingHours-Morning.pcap_ISCX.csv
Monday-WorkingHours.pcap_ISCX.csv
Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv
Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv
Tuesday-WorkingHours.pcap_ISCX.csv
Wednesday-workingHours.pcap_ISCX.csv
```

---

## Prétraitement des données

Le pipeline de prétraitement réalise notamment :

- chargement des différents fichiers CIC-IDS2017 ;
- nettoyage des noms de colonnes ;
- conversion des variables numériques ;
- gestion des valeurs infinies ;
- suppression des colonnes inutilisables ;
- normalisation des labels ;
- sélection des caractéristiques utilisées par les modèles ;
- séparation des données en ensembles d'entraînement et de test.

### Données utilisées dans l'expérience

L'expérience réalisée sur le dataset complet a produit :

| Élément | Valeur |
|---|---:|
| Flux d'entraînement | 2 017 889 |
| Flux de test | 504 473 |
| Caractéristiques sélectionnées | 35 |

---

## Modèles de Machine Learning

Trois modèles ont été étudiés :

1. Random Forest
2. Support Vector Machine
3. Réseau de neurones

### 1. Random Forest

Le Random Forest utilise un ensemble de 200 arbres de décision.

Une pondération des classes est utilisée afin de mieux prendre en compte les différences de représentation entre les classes.

Configuration principale :

```text
n_estimators = 200
class_weight = balanced
n_jobs = -1
```

### 2. Support Vector Machine

Un SVM avec un noyau RBF est utilisé.

Configuration principale :

```text
kernel = RBF
C = 1
gamma = scale
class_weight = balanced
```

#### Particularité de l'entraînement

L'entraînement d'un SVM RBF sur l'ensemble des environ 2 millions de flux serait très coûteux en temps et en ressources.

Pour cette raison, un **sous-échantillon stratifié de 5 000 flux** a été utilisé pour l'entraînement du SVM.

Cette différence doit être prise en compte lors de l'interprétation de la comparaison avec les autres modèles.

### 3. Réseau de neurones

Un perceptron multicouche (MLP) est utilisé comme modèle de réseau de neurones.

Architecture :

```text
Entrée
  │
  ▼
64 neurones
  │
  ▼
32 neurones
  │
  ▼
Sortie
```

Le modèle utilise également un mécanisme d'arrêt anticipé lorsque les conditions d'entraînement le permettent.

---

# Résultats expérimentaux

Les trois modèles ont été évalués sur le même ensemble de test de **504 473 flux**.

| Modèle | Accuracy | Precision | Recall | F1-score | FPR | Temps de prédiction |
|---|---:|---:|---:|---:|---:|---:|
| **Random Forest** | **99.76%** | **98.99%** | **99.58%** | **99.28%** | **0.21%** | **1.91 s** |
| Neural Network | 98.24% | 94.19% | 95.50% | 94.84% | 1.20% | 0.93 s |
| SVM | 93.53% | 81.95% | 79.11% | 80.50% | 3.54% | 44.03 s |

### Temps d'entraînement

| Modèle | Temps d'entraînement |
|---|---:|
| Random Forest | 327.38 s |
| Neural Network | 358.83 s |
| SVM | 2.22 s* |

\* Le SVM a été entraîné sur un sous-échantillon stratifié de 5 000 flux, contrairement au Random Forest et au réseau de neurones qui ont utilisé l'ensemble des données d'entraînement.

---

## Analyse des résultats

Dans cette configuration expérimentale, le **Random Forest obtient les meilleures performances globales**.

Il atteint :

- une accuracy de **99.76 %** ;
- une précision de **98.99 %** ;
- un recall de **99.58 %** ;
- un F1-score de **99.28 %** ;
- un taux de faux positifs de seulement **0.21 %**.

Le réseau de neurones obtient également de bonnes performances avec un F1-score de **94.84 %**.

Le SVM obtient des performances inférieures dans cette configuration, mais cette comparaison doit être interprétée avec prudence puisque son entraînement a été effectué sur seulement 5 000 flux.

Le temps d'entraînement du SVM ne peut donc pas être comparé directement aux temps d'entraînement des deux autres modèles.

---

## Détection de nouveaux flux

Le projet possède une couche de prédiction permettant d'utiliser un modèle entraîné pour classifier de nouveaux flux réseau.

Les entrées peuvent être fournies sous forme de fichier CSV ou JSON.

Chaque flux est classifié comme :

```text
NORMAL
```

ou :

```text
ATTACK
```

Lorsqu'elle est disponible, une estimation de confiance est également fournie.

### Exemple

Une expérience de prédiction sur cinq flux a produit :

```text
Flow #1    NORMAL
Flow #2    NORMAL
Flow #3    NORMAL
Flow #4    ATTACK
Flow #5    NORMAL
```

Le système peut également fournir une estimation de confiance pour chaque prédiction.

---

# Dashboard

Une interface graphique basée sur **Streamlit** permet d'interagir avec le système de détection.

Le dashboard permet notamment de :

- sélectionner un modèle ;
- charger des flux réseau ;
- effectuer des prédictions ;
- afficher la classification de chaque flux ;
- afficher la confiance associée lorsqu'elle est disponible ;
- compter les flux NORMAL et ATTACK ;
- visualiser les performances des modèles.

L'application principale se trouve dans :

```text
dashboard/app.py
```

Pour lancer le dashboard :

```bash
streamlit run dashboard/app.py
```

---

# Structure du projet

```text
intelligent-network-ids/
│
├── config/
│   └── config.yaml
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── docs/
│   ├── pdf_reference.md
│   └── technical_overview.md
│
├── models/
│
├── results/
│   ├── figures/
│   ├── metrics/
│   └── reports/
│
├── scripts/
│   ├── check_environment.py
│   ├── evaluate.py
│   ├── predict.py
│   ├── preprocess.py
│   ├── realtime_csv_watch.py
│   └── train.py
│
├── src/
│   ├── data/
│   │   └── loader.py
│   │
│   ├── evaluation/
│   │   └── metrics.py
│   │
│   ├── ids/
│   │   ├── predictor.py
│   │   └── realtime.py
│   │
│   ├── models/
│   │   └── trainers.py
│   │
│   ├── preprocessing/
│   │   └── pipeline.py
│   │
│   └── utils/
│       ├── io.py
│       └── paths.py
│
├── tests/
│   ├── test_loader.py
│   ├── test_prediction.py
│   └── test_preprocessing.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

# Installation

## 1. Cloner le dépôt

```bash
git clone https://github.com/aboudAG/intelligent-network-ids.git
cd intelligent-network-ids
```

## 2. Créer un environnement virtuel

### Linux / WSL

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

# Utilisation

## Vérifier l'environnement

```bash
python scripts/check_environment.py
```

---

## Préparer les données

Après avoir placé les fichiers CIC-IDS2017 dans :

```text
data/raw/
```

lancer :

```bash
python scripts/preprocess.py
```

Le pipeline génère les données nécessaires à l'entraînement dans :

```text
data/processed/
```

---

## Entraîner un modèle

### Random Forest

```bash
python scripts/train.py --model random_forest
```

### SVM

```bash
python scripts/train.py --model svm
```

### Réseau de neurones

```bash
python scripts/train.py --model neural_network
```

### Entraîner les trois modèles

```bash
python scripts/train.py --model all
```

Les modèles entraînés sont enregistrés localement dans :

```text
models/
```

Ces fichiers ne sont pas versionnés dans GitHub.

---

# Évaluation

Après l'entraînement :

```bash
python scripts/evaluate.py
```

Les métriques et graphiques sont générés localement dans :

```text
results/
```

Les principales métriques utilisées sont :

- Accuracy
- Precision
- Recall
- F1-score
- False Positive Rate
- Temps de prédiction
- Temps d'entraînement

---

# Prédiction

Pour effectuer une prédiction sur de nouveaux flux :

```bash
python scripts/predict.py \
    --model models/random_forest.joblib \
    --input data/sample/sample_cicids_like.csv
```

Le système charge le modèle sélectionné, aligne les caractéristiques d'entrée avec celles utilisées pendant l'entraînement et produit une prédiction pour chaque flux.

---

# Tests

Les tests unitaires peuvent être exécutés avec :

```bash
pytest
```

Les tests couvrent notamment :

- le chargement des données ;
- le prétraitement ;
- la préparation des données pour la prédiction.

---

# Prototype de détection en quasi temps réel

Le projet contient également un prototype permettant de surveiller un répertoire contenant des fichiers CSV et de traiter les nouveaux flux détectés.

Le script principal est :

```text
scripts/realtime_csv_watch.py
```

avec les composants correspondants dans :

```text
src/ids/realtime.py
```

Exemple :

```bash
python scripts/realtime_csv_watch.py \
    --input-dir data/live \
    --model models/random_forest.joblib
```

Cette fonctionnalité constitue un **prototype de traitement en quasi temps réel** à partir de données CSV.

Elle ne doit pas être considérée comme une capture directe du trafic réseau sur une infrastructure de production.

---

# Limites expérimentales

## Comparaison du SVM

Le SVM a été entraîné sur un sous-échantillon stratifié de 5 000 flux alors que le Random Forest et le réseau de neurones ont été entraînés sur l'ensemble des données d'entraînement.

Les performances et les temps d'entraînement ne doivent donc pas être interprétés comme une comparaison parfaitement équitable entre trois entraînements réalisés dans les mêmes conditions.

## Déploiement réel

Le projet constitue un prototype expérimental.

Il ne s'agit pas encore d'un IDS directement déployé sur une infrastructure réseau réelle.

---

# Perspectives

Plusieurs améliorations peuvent être envisagées :

- optimisation des hyperparamètres ;
- expérimentation avec d'autres algorithmes de Machine Learning ;
- étude plus approfondie du déséquilibre des classes ;
- validation sur d'autres datasets réseau ;
- expérimentation avec des modèles de Deep Learning plus avancés ;
- amélioration du prototype de détection en quasi temps réel ;
- intégration avec des sources de trafic réseau réelles ;
- comparaison avec une approche IDS traditionnelle basée sur les signatures ;
- amélioration de l'interprétabilité des décisions du modèle ;
- étude des performances dans un environnement de déploiement réel.

---

# Technologies utilisées

- **Python**
- **Pandas**
- **NumPy**
- **Scikit-learn**
- **Matplotlib**
- **Seaborn**
- **Streamlit**
- **Pytest**
- **Git**
- **GitHub**

---

# Organisation du code

Le projet est organisé selon plusieurs composants afin de séparer les responsabilités :

| Répertoire | Rôle |
|---|---|
| `src/data/` | Chargement des données |
| `src/preprocessing/` | Prétraitement et préparation des données |
| `src/models/` | Entraînement et gestion des modèles |
| `src/evaluation/` | Calcul et sauvegarde des métriques |
| `src/ids/` | Prédiction et logique IDS |
| `src/utils/` | Fonctions utilitaires |
| `scripts/` | Points d'entrée pour exécuter le pipeline |
| `dashboard/` | Interface Streamlit |
| `tests/` | Tests automatisés |
| `docs/` | Documentation technique |

---

# Gestion des données et modèles

Les fichiers volumineux ne sont volontairement pas versionnés dans Git.

Sont notamment exclus :

```text
data/raw/
data/processed/
models/*.joblib
results/figures/
results/metrics/
results/reports/
```

Cela permet de conserver un dépôt GitHub léger tout en permettant de reproduire le pipeline à partir des données et des instructions nécessaires.

---

# Auteur

**aboudAG**

Projet académique et portfolio en réseaux, systèmes et cybersécurité.

---

# Licence

Ce projet est distribué sous licence MIT.
