# MONITORING_API

Documentation du projet.

MONITORING_API/
├── data/                         # Dossier pour les datasets
│   ├── train.csv                 # Jeu d'entraînement
│   ├── test.csv                  # Jeu de test
│   ├── reference.csv             # Jeu de référence
├── models/                       # Dossier pour sauvegarder les modèles entraînés
│   ├── model.pkl                 # Modèle entraîné (Pickle ou autre format)
├── src/                          # Code source principal
│   ├── api/                      # API FastAPI
│   │   ├── main.py               # Code principal de l'API
│   │   ├── predict.py            # Endpoint de prédiction
│   │   ├── metrics.py            # Intégration avec Prometheus
│   ├── training/                 # Scripts d'entraînement et d'évaluation
│   │   ├── train_model.py        # Script pour entraîner le modèle
│   │   ├── evaluate_model.py     # Script pour évaluer le modèle
│   ├── monitoring/               # Scripts pour Evidently AI
│   │   ├── monitor_drift.py      # Analyse des dérives
│   │   ├── generate_reports.py   # Génération de rapports
├── dashboards/                   # Configurations Grafana
│   ├── grafana_dashboard.json    # Fichier de configuration pour Grafana
├── config/                       # Fichiers de configuration
│   ├── prometheus.yml            # Configuration pour Prometheus
│   ├── settings.json             # Configuration générale (ex. ports)
├── docker/                       # Configurations pour Docker
│   ├── Dockerfile.api            # Dockerfile pour l’API
│   ├── Dockerfile.prometheus     # Dockerfile pour Prometheus (optionnel)
│   ├── Dockerfile.grafana        # Dockerfile pour Grafana (optionnel)
├── docker-compose.yml            # Fichier Docker Compose pour orchestrer tout
├── tests/                        # Tests unitaires
│   ├── test_api.py               # Tests pour l'API
│   ├── test_training.py          # Tests pour le modèle
├── README.md                     # Documentation du projet
├── requirements.txt              # Dépendances Python
└── .env                          # Variables d'environnement


---

### **Description du dataset Iris**

Le dataset **Iris** est l'un des ensembles de données les plus célèbres en machine learning. Il contient des informations sur trois espèces de fleurs d'iris, avec des mesures physiques pour chaque échantillon.

#### **1. Caractéristiques principales :**
- **Nombre d'échantillons** : 150 (50 pour chaque espèce de fleur).
- **Nombre de features** : 4 (toutes des variables numériques).
- **Classe cible** : Espèce de la fleur, avec trois catégories.

#### **2. Colonnes du dataset :**

| **Feature**         | **Description**                    | **Unité** |
|----------------------|------------------------------------|-----------|
| `sepal length (cm)`  | Longueur du sépale                | Centimètres |
| `sepal width (cm)`   | Largeur du sépale                 | Centimètres |
| `petal length (cm)`  | Longueur du pétale                | Centimètres |
| `petal width (cm)`   | Largeur du pétale                 | Centimètres |
| `target`             | Classe cible (espèce de la fleur) | -         |

#### **3. Classes cibles :**
- Les valeurs dans la colonne **`target`** représentent les trois espèces d’iris :
  - **0** : Iris-setosa
  - **1** : Iris-versicolor
  - **2** : Iris-virginica

#### **4. Exemple de données :**

| `sepal length (cm)` | `sepal width (cm)` | `petal length (cm)` | `petal width (cm)` | `target` |
|----------------------|--------------------|----------------------|--------------------|----------|
| 5.1                  | 3.5               | 1.4                  | 0.2                | 0        |
| 7.0                  | 3.2               | 4.7                  | 1.4                | 1        |
| 6.3                  | 3.3               | 6.0                  | 2.5                | 2        |

#### **5. Objectif du projet :**
L'objectif est de construire un modèle de machine learning capable de prédire l'espèce de la fleur (classe cible) à partir des quatre mesures physiques (features). Ce modèle est ensuite intégré dans une API FastAPI pour permettre des prédictions en temps réel.

---

