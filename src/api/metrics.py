from fastapi import APIRouter
from prometheus_fastapi_instrumentator import Instrumentator

# Créer un routeur pour les métriques
metrics_router = APIRouter()

# Initialiser l'instrumentateur Prometheus
instrumentator = Instrumentator()

# Ajouter les métriques de Prometheus
@metrics_router.get(
    "/",
    summary="Exposer les métriques Prometheus",
    description=(
        "Cet endpoint expose les métriques collectées pour surveiller l'API. "
        "Il est conçu pour être consommé par Prometheus."
    ),
    include_in_schema=False  # Facultatif si vous ne souhaitez pas l'inclure dans Swagger
)
async def prometheus_metrics():
    """
    Endpoint exposant les métriques au format compatible avec Prometheus.
    """
    pass  # Les métriques sont gérées automatiquement par Prometheus FastAPI Instrumentator


# Configuration de l'instrumentateur Prometheus
def configure_metrics(app):
    """
    Configure l'instrumentation Prometheus pour l'application FastAPI.

    :param app: Instance FastAPI à instrumenter.
    """
    instrumentator.instrument(app).expose(app)
