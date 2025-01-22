from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from src.api.predict import predict_router  # Importer le routeur des prédictions
from src.api.metrics import metrics_router  # Importer le routeur des métriques
from src.monitoring.evidently_monitor import update_drift_metrics  # Utiliser la fonction correcte
import pandas as pd
import sys
import os

# Ajoutez le chemin racine au PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

# Chemin des données pour la surveillance Evidently
REFERENCE_DATA_PATH = "/app/data/reference.csv"
CURRENT_DATA_PATH = "/app/data/current.csv"

# Vérification et création des fichiers nécessaires
if not os.path.exists(CURRENT_DATA_PATH):
    print(f"Le fichier {CURRENT_DATA_PATH} est manquant. Création d'un fichier vide.")
    # Créez un fichier current.csv vide avec les colonnes attendues
    empty_df = pd.DataFrame(columns=["sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)"])
    empty_df.to_csv(CURRENT_DATA_PATH, index=False)

if not os.path.exists(REFERENCE_DATA_PATH):
    raise RuntimeError(f"Le fichier {REFERENCE_DATA_PATH} est manquant. Impossible de continuer.")

print(f"Chemin absolu du fichier de référence : {REFERENCE_DATA_PATH}")
print(f"Le fichier de référence existe ? {os.path.exists(REFERENCE_DATA_PATH)}")
print(f"Chemin absolu du fichier actuel : {CURRENT_DATA_PATH}")
print(f"Le fichier actuel existe ? {os.path.exists(CURRENT_DATA_PATH)}")

# Charger les données de référence et actuelles pour Evidently
try:
    reference_data = pd.read_csv(REFERENCE_DATA_PATH)
    current_data = pd.read_csv(CURRENT_DATA_PATH)
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement des fichiers : {str(e)}")

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
        update_drift_metrics(reference_data, current_data)  # Utiliser la fonction correcte
        return {"message": "Concept drift calculé et métriques mises à jour avec succès."}
    except Exception as e:
        return {"error": str(e), "message": "Une erreur est survenue lors du calcul du concept drift."}
