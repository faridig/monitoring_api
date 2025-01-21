# Script pour entraîner le modèle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Charger le dataset d'entraînement
train_data = pd.read_csv("data/train.csv")

# Séparer les features (X) et la cible (y)
X = train_data.drop("target", axis=1)
y = train_data["target"]

# Entraîner un modèle Random Forest
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Créer le dossier "models" s'il n'existe pas
os.makedirs("models", exist_ok=True)

# Sauvegarder le modèle dans un fichier
joblib.dump(model, "models/model.pkl")

print("Le modèle a été entraîné et sauvegardé dans 'models/model.pkl'.")
