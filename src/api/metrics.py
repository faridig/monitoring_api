from fastapi import APIRouter, FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge

# Créer un routeur pour les métriques
metrics_router = APIRouter()

# Déclaration des métriques personnalisées
prediction_count = Counter(
    "prediction_count_total", "Nombre total de prédictions effectuées"
)
latency_histogram = Histogram(
    "model_latency_seconds", "Durée de la prédiction (en secondes)"
)
error_count = Counter(
    "prediction_errors_total", "Nombre total d'erreurs de prédiction"
)
concept_drift_detected = Gauge(
    "concept_drift_detected", "Indicateur de concept drift détecté (1 si détecté, sinon 0)"
)
drift_magnitude = Gauge(
    "drift_magnitude", "Magnitude du concept drift détecté (si applicable)"
)

# Initialiser l'instrumentateur Prometheus
instrumentator = Instrumentator()

# Ajouter les métriques Prometheus
@metrics_router.get(
    "/metrics",
    summary="Exposer les métriques Prometheus",
    description=(
        "Cet endpoint expose les métriques collectées pour surveiller l'API. "
        "Il est conçu pour être consommé par Prometheus."
    ),
    include_in_schema=False,  # Facultatif si vous ne souhaitez pas l'inclure dans Swagger
)
async def prometheus_metrics():
    """
    Endpoint exposant les métriques au format compatible avec Prometheus.
    """
    pass  # Les métriques sont gérées automatiquement par Prometheus FastAPI Instrumentator


# Enregistrement des métriques personnalisées lors des prédictions
def record_prediction_metrics(latency: float, success: bool):
    """
    Enregistre des métriques personnalisées après une prédiction.

    :param latency: Temps pris pour effectuer la prédiction (en secondes).
    :param success: Indique si la prédiction a réussi ou échoué.
    """
    prediction_count.inc()  # Incrémenter le compteur de prédictions
    latency_histogram.observe(latency)  # Enregistrer la latence
    if not success:
        error_count.inc()  # Incrémenter le compteur d'erreurs


# Mise à jour des métriques de concept drift
def update_drift_metrics(drift_detected: bool, magnitude: float = 0.0):
    """
    Met à jour les métriques associées au concept drift.

    :param drift_detected: Indique si un concept drift a été détecté (True/False).
    :param magnitude: Magnitude du concept drift détecté.
    """
    concept_drift_detected.set(1 if drift_detected else 0)  # Indique si un drift est détecté
    drift_magnitude.set(magnitude)  # Enregistre la magnitude du drift


# Configuration de l'instrumentateur Prometheus
def configure_metrics(app: FastAPI):
    """
    Configure l'instrumentation Prometheus pour l'application FastAPI.

    :param app: Instance FastAPI à instrumenter.
    """
    instrumentator.instrument(app).expose(app)
