from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from src.api.predict import predict_router  # Importer le routeur des prédictions
from api.metrics import metrics_router  # Importer le routeur des métriques
from src.monitoring.evidently_monitor import calculate_and_update_metrics  # Importer les fonctions Evidently
import pandas as pd

# Chemin des données pour la surveillance Evidently
REFERENCE_DATA_PATH = "data/reference.csv"
CURRENT_DATA_PATH = "data/current.csv"

# Charger les données de référence et actuelles pour Evidently
try:
    reference_data = pd.read_csv(REFERENCE_DATA_PATH)
    current_data = pd.read_csv(CURRENT_DATA_PATH)
except FileNotFoundError:
    raise RuntimeError(
        f"Les fichiers nécessaires pour Evidently ({REFERENCE_DATA_PATH} ou {CURRENT_DATA_PATH}) sont introuvables."
    )

# Créer une instance FastAPI
app = FastAPI(
    title="API de Monitoring et Prédiction",
    description="""
    Cette API permet :
    - De surveiller les métriques via Prometheus.
    - De détecter le concept drift via Evidently.
    - D'effectuer des prédictions basées sur un modèle de machine learning.
    """,
    version="1.1.0",
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


# Endpoint pour surveiller le concept drift avec Evidently
@app.post("/monitor/drift", summary="Surveiller le concept drift")
def monitor_drift():
    """
    Utilise Evidently pour calculer les métriques de concept drift
    entre les données de référence et les données actuelles.
    """
    try:
        calculate_and_update_metrics(reference_data, current_data)
        return {"message": "Concept drift calculé et métriques mises à jour avec succès."}
    except Exception as e:
        return {"error": str(e), "message": "Une erreur est survenue lors du calcul du concept drift."}
