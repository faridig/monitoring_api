# Monitoring API

## Description
Cette application est conçue pour :
- **Surveiller les métriques de performance et de qualité des données** à l'aide de **Prometheus** et **Grafana**.
- **Détecter les dérives de données (concept drift)** en utilisant la bibliothèque **Evidently**.
- **Effectuer des prédictions** avec un modèle de machine learning entraîné.

Le projet utilise **FastAPI** pour exposer une API REST et **Docker** pour simplifier le déploiement.

---

## Fonctionnalités principales
1. **Surveillance des métriques :**
   - Latence des prédictions.
   - Nombre total de prédictions.
   - Taux d'erreurs.
   - Détection de dérive des données (concept drift).
   - Visualisation des métriques dans Grafana.

2. **Prédictions en temps réel :**
   - Recevez des caractéristiques (longueur/largeur des sépales et pétales) et obtenez une prédiction de la classe Iris.

3. **Détection de dérive des données :**
   - Analyse de la dérive entre les données actuelles et les données de référence.
   - Mise à jour des métriques en cas de dérive détectée.

4. **Modèle machine learning :**
   - Entraîné sur un jeu de données Iris avec un modèle **Random Forest**.

---

## Structure du projet

```
monitoring_api/
├── data/                 # Données utilisées pour le modèle et le monitoring
│   ├── train.csv         # Données d'entraînement
│   ├── test.csv          # Données de test
│   ├── current.csv       # Données actuelles pour la surveillance
│   └── reference.csv     # Données de référence pour le monitoring
├── models/               # Modèle entraîné
│   └── model.pkl         # Modèle Random Forest sauvegardé
├── src/                  # Code source
│   ├── api/              # API FastAPI
│   │   ├── main.py       # Point d'entrée principal de l'API
│   │   ├── metrics.py    # Gestion des métriques
│   │   └── predict.py    # Gestion des prédictions
│   ├── monitoring/       # Détection de dérive avec Evidently
│   │   └── evidently_monitor.py
│   └── training/         # Scripts d'entraînement et d'évaluation
│       ├── train_model.py
│       └── evaluate_model.py
├── grafana/              # Configuration de Grafana
│   ├── provisioning/
│   │   ├── dashboards/  # Tableau de bord Grafana
│   │   └── datasources/ # Configuration des sources de données
├── prometheus.yml        # Configuration de Prometheus
├── docker-compose.yml    # Orchestration des services Docker
├── Dockerfile            # Construction de l'image Docker
└── README.md             # Documentation (ce fichier)
```

---

## Flux d'interaction

1. **Entraînement du modèle :**
   - **`src/training/train_model.py`** : Entraîne un modèle Random Forest sur **`data/train.csv`**.
   - Le modèle est sauvegardé dans **`models/model.pkl`**.

2. **Prédictions via l'API :**
   - L'API (**`src/api/main.py`**) expose un endpoint `/predict`.
   - **`src/api/predict.py`** :
     - Charge le modèle.
     - Accepte les caractéristiques d'une fleur Iris et retourne la classe prédite.
     - Sauvegarde les données reçues dans **`data/current.csv`**.
   - Enregistre des métriques sur la latence et les erreurs via **`metrics.py`**.

3. **Surveillance des dérives :**
   - L'endpoint `/monitor/drift` (défini dans **`src/api/main.py`**) :
     - Compare **`data/reference.csv`** (baseline) et **`data/current.csv`** (nouvelles données).
     - **`src/monitoring/evidently_monitor.py`** analyse les dérives à l'aide de **Evidently**.
     - Met à jour les métriques de dérive via **`metrics.py`**.

4. **Visualisation des métriques :**
   - **Prometheus** collecte toutes les métriques exposées par l'API.
   - **Grafana** visualise les métriques grâce aux configurations dans **`grafana/provisioning`**.

---

## Métriques exposées
Voici les métriques surveillées dans le système :

1. **Prédictions** :
   - **`prediction_count_total`** : Nombre total de prédictions effectuées.
   - **`model_latency_seconds`** : Latence des prédictions (en secondes).
   - **`prediction_errors_total`** : Nombre total d'erreurs de prédiction.

2. **Dérives des données** :
   - **`concept_drift_detected`** : Indique si une dérive est détectée (1 = Oui, 0 = Non).
   - **`drift_magnitude`** : Magnitude de la dérive détectée.
   - **`dataset_drift_score`** : Proportion des colonnes affectées par une dérive.
   - **`dataset_drift_detected`** : Indique si une dérive globale est détectée.

---

## Installation et exécution

### Prérequis
- **Docker** et **docker-compose** doivent être installés.

### Étapes
1. Clonez le projet :
   ```bash
   git clone https://github.com/faridig/monitoring_api.git
   cd monitoring_api
   ```

2. Construisez et démarrez les services Docker :
   ```bash
   docker-compose up --build
   ```

3. Accédez à l'API :
   - Swagger : [http://localhost:8000/docs](http://localhost:8000/docs)
   - Endpoint `/predict` pour faire des prédictions.
   - Endpoint `/monitor/drift` pour surveiller les dérives.

4. Accédez à Grafana :
   - URL : [http://localhost:3000](http://localhost:3000)
   - Connectez-vous (par défaut : admin/admin).
   - Visualisez le tableau de bord provisionné.

---

## Exemple d'utilisation

### Faire une prédiction
Endpoint : **`POST /predict`**

#### Entrée :
```json
{
  "sepal_length_cm": 5.1,
  "sepal_width_cm": 3.5,
  "petal_length_cm": 1.4,
  "petal_width_cm": 0.2
}
```

#### Réponse :
```json
{
  "prediction": 0
}
```

### Détecter une dérive
Endpoint : **`POST /monitor/drift`**

#### Réponse :
```json
{
  "message": "Concept drift calculé et métriques mises à jour avec succès."
}
```

---

## Contributions
Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet, n'hésitez pas à soumettre une pull request ou à ouvrir une issue.

---

## Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.

