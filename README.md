
# MONITORING_API

Ce projet propose un système de surveillance pour un modèle de machine learning, avec une API pour les prédictions, des outils de détection de dérives de données, et des tableaux de bord de suivi des performances.

## Fonctionnalités principales

- **Surveillance des performances** : Suivi des métriques clés et détection d'anomalies.
- **Détection des dérives de données** : Comparaison entre données de référence et nouvelles données.
- **API pour les prédictions** : Accès rapide et facile aux prédictions via FastAPI.

## Structure du projet

```
MONITORING_API/
├── data/                   # Dossier pour les jeux de données
│   ├── train.csv           # Jeu de données d'entraînement
│   ├── test.csv            # Jeu de données de test
│   └── reference.csv       # Jeu de données de référence
├── models/                 # Dossier pour les modèles entraînés
│   └── model.pkl           # Modèle entraîné (format Pickle)
├── src/                    # Code source principal
│   ├── api/                # API FastAPI
│   │   ├── main.py         # Code principal de l'API
│   │   ├── predict.py      # Endpoint de prédiction
│   │   └── metrics.py      # Intégration avec Prometheus
│   ├── training/           # Scripts d'entraînement et d'évaluation
│   │   ├── train_model.py  # Script pour entraîner le modèle
│   │   └── evaluate_model.py # Script pour évaluer le modèle
│   └── monitoring/         # Scripts pour Evidently AI
│       ├── monitor_drift.py # Analyse des dérives
│       └── generate_reports.py # Génération de rapports
├── grafana/                # Configuration pour Grafana
│   └── provisioning/
│       ├── dashboards/     # Tableaux de bord Grafana
│       └── datasources/    # Sources de données Grafana
├── Dockerfile              # Fichier Docker pour l'application
├── docker-compose.yml      # Configuration Docker Compose
├── prometheus.yml          # Configuration de Prometheus
├── requirements.txt        # Liste des dépendances Python
└── README.md               # Documentation du projet
```

## Structure des données

- `train.csv` : Données d'entraînement.
- `test.csv` : Données de test pour évaluation.
- `reference.csv` : Données de référence pour surveiller les dérives.

Placez ces fichiers dans le dossier `data/` avant l'utilisation.

## Installation

1. Clonez le projet et installez les dépendances :
   ```bash
   git clone https://github.com/faridig/monitoring_api.git
   cd monitoring_api
   pip install -r requirements.txt
   ```

2. Lancez les services :
   ```bash
   docker-compose up -d
   ```

## Utilisation

### Entraîner le modèle

Lancez l'entraînement avec :
```bash
python src/training/train_model.py
```

### API de prédictions

Démarrez l'API FastAPI :
```bash
python src/api/main.py
```
Accédez à `http://localhost:8000` pour les prédictions ou à la documentation API sur `/docs`.

### Surveillance des métriques

- **Prometheus** : `http://localhost:9090`
- **Grafana** : `http://localhost:3000` (Identifiants par défaut : `admin/admin`)

### Détection de dérives

Analysez les dérives de données avec :
```bash
python src/monitoring/monitor_drift.py
```

## Tests

Exécutez les tests unitaires avec :
```bash
pytest
```

## Contribution

Contributions bienvenues via *issues* ou *pull requests*.

## Licence

Ce projet est sous licence MIT.
