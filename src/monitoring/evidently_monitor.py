import pandas as pd
from prometheus_client import Gauge
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import DatasetDriftMetric

# Initialiser les métriques Prometheus pour le drift
drift_gauge = Gauge(
    "dataset_drift_score",
    "Score de drift détecté sur le dataset"
)
drift_detected_gauge = Gauge(
    "dataset_drift_detected",
    "Indique si un drift significatif a été détecté (1 = Oui, 0 = Non)"
)

# Configurer Evidently pour le suivi du drift
column_mapping = ColumnMapping(
    target=None,  # Si vous avez une cible dans les données, précisez-la ici
    prediction=None,  # Si vous avez des prédictions, précisez leur colonne
    numerical_features=["sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)"]
)

drift_report = Report(metrics=[DatasetDriftMetric()])

def update_drift_metrics(reference_data: pd.DataFrame, current_data: pd.DataFrame):
    """
    Met à jour les métriques Prometheus pour surveiller le drift.

    :param reference_data: Jeu de données de référence (historique ou baseline).
    :param current_data: Nouveau jeu de données (données en temps réel).
    """
    # Générer un rapport Evidently basé sur les données
    drift_report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)
    
    # Extraire les résultats de drift
    results = drift_report.as_dict()
    drift_score = results["metrics"][0]["result"]["dataset_drift"]["drift_score"]
    drift_detected = results["metrics"][0]["result"]["dataset_drift"]["drift_detected"]
    
    # Mettre à jour les métriques Prometheus
    drift_gauge.set(drift_score)  # Score de drift
    drift_detected_gauge.set(1 if drift_detected else 0)  # 1 = Drift détecté, 0 = Pas de drift
