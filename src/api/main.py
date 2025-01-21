from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from src.api.predict import predict_router  # Importer le routeur des prédictions
from src.api.metrics import metrics_router  # Importer le routeur des métriques

# Créer une instance FastAPI
app = FastAPI(
    title="API de Monitoring et Prédiction",
    description="""
    Cette API permet :
    - De surveiller les métriques via Prometheus.
    - D'effectuer des prédictions basées sur un modèle de machine learning.
    """,
    version="1.0.0",
    contact={
        "name": "Farid",
        "email": "farid@example.com",
    },
    license_info={
        "name": "MIT",
    },
)


# Instrumentation pour Prometheus
Instrumentator().instrument(app).expose(app)

# Inclure les routeurs
app.include_router(predict_router, prefix="/predict", tags=["Predictions"])
app.include_router(metrics_router, prefix="/metrics", tags=["Metrics"])

# Endpoint racine pour vérifier que l'API fonctionne
@app.get("/", summary="Bienvenue dans l'API")
def read_root():
    """
    Endpoint pour tester que l'API fonctionne correctement.
    """
    return {"message": "Bienvenue dans l'API de monitoring et de prédiction !"}

