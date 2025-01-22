from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import time
import os
from src.api.metrics import record_prediction_metrics  # Importer la fonction pour enregistrer les métriques

# Charger le modèle
MODEL_PATH = "models/model.pkl"
CURRENT_DATA_PATH = "data/current.csv"
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise RuntimeError(f"Le fichier modèle '{MODEL_PATH}' est introuvable.")

# Mapper les noms des colonnes envoyées à l'API vers ceux vus par le modèle
FEATURE_MAPPING = {
    "sepal_length_cm": "sepal length (cm)",
    "sepal_width_cm": "sepal width (cm)",
    "petal_length_cm": "petal length (cm)",
    "petal_width_cm": "petal width (cm)",
}

# Définir un modèle pour valider les données envoyées à l'API
class PredictionRequest(BaseModel):
    sepal_length_cm: float
    sepal_width_cm: float
    petal_length_cm: float
    petal_width_cm: float

class PredictionResponse(BaseModel):
    prediction: int

# Créer un routeur pour les prédictions
predict_router = APIRouter()

def save_to_current_csv(data: pd.DataFrame, file_path: str):
    """
    Sauvegarde ou met à jour les données dans le fichier current.csv.

    :param data: Données reçues sous forme de DataFrame.
    :param file_path: Chemin du fichier à mettre à jour.
    """
    if not os.path.exists(file_path):  # Vérifie si le fichier n'existe pas
        data.to_csv(file_path, index=False)  # Crée le fichier avec les données reçues
    else:
        existing_data = pd.read_csv(file_path)  # Charge les données existantes
        updated_data = pd.concat([existing_data, data], ignore_index=True)  # Ajoute les nouvelles données
        updated_data.to_csv(file_path, index=False)  # Sauvegarde les données mises à jour

@predict_router.post(
    "/",
    summary="Effectuer une prédiction",
    description=(
        "Cet endpoint reçoit les caractéristiques d'une fleur Iris et retourne l'espèce prédite.\n\n"
        "### Paramètres d'entrée :\n"
        "- `sepal_length_cm` (float) : Longueur du sépale en cm.\n"
        "- `sepal_width_cm` (float) : Largeur du sépale en cm.\n"
        "- `petal_length_cm` (float) : Longueur du pétale en cm.\n"
        "- `petal_width_cm` (float) : Largeur du pétale en cm.\n\n"
        "### Réponse :\n"
        "- `prediction` (int) : Classe prédite.\n"
        "  - `0` : Iris-setosa\n"
        "  - `1` : Iris-versicolor\n"
        "  - `2` : Iris-virginica\n"
    ),
    response_description="Prédiction basée sur les données fournies",
    response_model=PredictionResponse,
    responses={
        200: {
            "description": "Prédiction réussie",
            "content": {
                "application/json": {
                    "example": {"prediction": 0}
                }
            },
        },
        422: {
            "description": "Erreur de validation des données",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "sepal_length_cm"],
                                "msg": "value is not a valid float",
                                "type": "type_error.float",
                            }
                        ]
                    }
                },
            },
        },
        500: {
            "description": "Erreur lors de la prédiction",
            "content": {
                "application/json": {
                    "example": {"detail": "Une erreur est survenue lors de la prédiction."}
                }
            },
        },
    },
)
def predict(request: PredictionRequest):
    """
    Effectue une prédiction basée sur les caractéristiques d'une fleur Iris.
    """
    start_time = time.time()  # Démarre le suivi de la latence
    success = True

    try:
        # Convertir les données reçues en DataFrame
        input_data = pd.DataFrame([request.dict()])
        
        # Renommer les colonnes pour correspondre à celles utilisées par le modèle
        input_data = input_data.rename(columns=FEATURE_MAPPING)
        
        # Faire une prédiction avec le modèle
        prediction = model.predict(input_data)[0]

        # Sauvegarder les données dans current.csv
        save_to_current_csv(input_data, CURRENT_DATA_PATH)

    except Exception as e:
        success = False
        # Enregistrer la métrique d'erreur
        record_prediction_metrics(latency=0, success=success)
        raise HTTPException(status_code=500, detail="Une erreur est survenue lors de la prédiction.")
    
    latency = time.time() - start_time  # Calculer la latence
    # Enregistrer les métriques
    record_prediction_metrics(latency=latency, success=success)

    return {"prediction": int(prediction)}
