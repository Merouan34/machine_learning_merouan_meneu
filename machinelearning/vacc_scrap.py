import pandas as pd
import requests
import os

# URL du fichier CSV mis à jour quotidiennement
VACCINE_CSV_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

def fetch_vaccination_data():
    """Télécharge et extrait les données de vaccination"""
    print("📥 Téléchargement des données de vaccination...")
    
    try:
        response = requests.get(VACCINE_CSV_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Erreur de connexion : {e}")
        return

    # Sauvegarder le fichier brut localement
    raw_csv_path = "data/raw_vaccination_data.csv"
    with open(raw_csv_path, "wb") as file:
        file.write(response.content)

    print("✅ Téléchargement terminé !")

    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv(raw_csv_path, usecols=["location", "date", "total_vaccinations", "people_fully_vaccinated_per_hundred"])
    
    # Garder uniquement les dernières valeurs par pays
    df = df.sort_values(by=["location", "date"]).groupby("location").last().reset_index()

    # Renommer les colonnes pour la clarté
    df = df.rename(columns={
        "location": "Country",
        "total_vaccinations": "Total_Vaccinations",
        "people_fully_vaccinated_per_hundred": "Vaccinated_Percent"
    })

    # Supprimer les lignes où le taux de vaccination est NaN
    df = df.dropna(subset=["Vaccinated_Percent"])

    # Supprimer les anciennes données brutes
    os.remove(raw_csv_path)

    # Sauvegarder le fichier nettoyé
    vaccine_data_path = "data/vaccination_data.csv"
    if os.path.exists(vaccine_data_path):
        os.remove(vaccine_data_path)

    df.to_csv(vaccine_data_path, index=False)

    print("\n✅ Données de vaccination enregistrées dans 'data/vaccination_data.csv'")
    print("\n🔎 Vérification des 10 premières lignes :")
    print(df.head(10))

# Exécuter le téléchargement
fetch_vaccination_data()
