# Script pour évaluer le modèle
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Charger le modèle sauvegardé
model = joblib.load("models/model.pkl")

# Charger les données de test
test_data = pd.read_csv("data/test.csv")

# Séparer les features (X) et les labels (y)
X_test = test_data.drop("target", axis=1)
y_test = test_data["target"]

# Faire des prédictions sur les données de test
y_pred = model.predict(X_test)

# Évaluer les performances
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Afficher les résultats
print(f"Précision : {accuracy:.2f}")
print("\nRapport de classification :\n", report)
print("\nMatrice de confusion :\n", conf_matrix)
