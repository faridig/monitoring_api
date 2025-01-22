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

# Initialiser le rapport Evidently
drift_report = Report(metrics=[DatasetDriftMetric()])

def preprocess_data(reference_data: pd.DataFrame, current_data: pd.DataFrame):
    """
    Prétraiter les données pour éviter les colonnes vides ou inutilisables.

    :param reference_data: Jeu de données de référence.
    :param current_data: Nouveau jeu de données.
    :return: Données nettoyées et prêtes pour le calcul.
    """
    print("Prétraitement des données...")
    print(f"Colonnes des données de référence avant nettoyage : {reference_data.columns.tolist()}")
    print(f"Colonnes des données actuelles avant nettoyage : {current_data.columns.tolist()}")

    # Supprimer les colonnes entièrement vides
    reference_data = reference_data.dropna(axis=1, how="all")
    current_data = current_data.dropna(axis=1, how="all")

    print(f"Colonnes des données de référence après nettoyage : {reference_data.columns.tolist()}")
    print(f"Colonnes des données actuelles après nettoyage : {current_data.columns.tolist()}")

    # Vérifier si les données sont vides
    if reference_data.empty or current_data.empty:
        raise ValueError("Les données de référence ou actuelles sont vides après le prétraitement.")

    # Vérifier les NaN dans les colonnes restantes
    print("NaN dans les données de référence :")
    print(reference_data.isna().sum())
    print("NaN dans les données actuelles :")
    print(current_data.isna().sum())

    return reference_data, current_data

def update_drift_metrics(reference_data: pd.DataFrame, current_data: pd.DataFrame):
    """
    Met à jour les métriques Prometheus pour surveiller le drift.

    :param reference_data: Jeu de données de référence (historique ou baseline).
    :param current_data: Nouveau jeu de données (données en temps réel).
    """
    try:
        print("Mise à jour des métriques de drift...")
        # Prétraiter les données
        reference_data, current_data = preprocess_data(reference_data, current_data)

        print("Données de référence prêtes :", reference_data.head())
        print("Données actuelles prêtes :", current_data.head())

        # Générer un rapport Evidently basé sur les données
        drift_report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)

        # Extraire les résultats de drift
        results = drift_report.as_dict()
        print("Rapport Evidently complet :", results)

        if "metrics" in results and len(results["metrics"]) > 0:
            drift_results = results["metrics"][0]["result"]
            print("Résultats du drift :", drift_results)

            drift_score = drift_results.get("share_of_drifted_columns", 0)
            drift_detected = drift_results.get("dataset_drift", False)

            # Mettre à jour les métriques Prometheus
            drift_gauge.set(drift_score)  # Score de drift
            drift_detected_gauge.set(1 if drift_detected else 0)  # 1 = Drift détecté, 0 = Pas de drift
        else:
            print("Aucune métrique de drift trouvée dans le rapport.")
            drift_gauge.set(0)
            drift_detected_gauge.set(0)

    except ValueError as e:
        print(f"Erreur lors du prétraitement des données : {e}")
        drift_gauge.set(0)  # Réinitialiser le score de drift
        drift_detected_gauge.set(0)  # Pas de drift
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        drift_gauge.set(0)  # Réinitialiser le score de drift
        drift_detected_gauge.set(0)  # Pas de drift
