import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Charger le dataset Iris
iris = load_iris()
data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
data['target'] = iris.target

# Division des données
train_data, temp_data = train_test_split(data, test_size=0.4, random_state=42)
reference_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42)

# Créer le dossier "data" s'il n'existe pas
import os
os.makedirs("data", exist_ok=True)

# Sauvegarder les datasets
train_data.to_csv("data/train.csv", index=False)
reference_data.to_csv("data/reference.csv", index=False)
test_data.to_csv("data/test.csv", index=False)

print("Les datasets ont été préparés et sauvegardés dans le dossier 'data/'.")
