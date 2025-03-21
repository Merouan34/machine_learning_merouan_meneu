import pandas as pd
import os

# Charger les datasets
covid_data_path = "data/covid_data_all_countries.csv"
vaccine_data_path = "data/vaccination_data.csv"
merged_data_path = "data/covid_vaccine_data.csv"

def merge_datasets():
    """Fusionne les données COVID avec les données de vaccination"""
    print("📥 Chargement des fichiers...")

    try:
        df_covid = pd.read_csv(covid_data_path)
        df_vaccine = pd.read_csv(vaccine_data_path)
    except FileNotFoundError as e:
        print(f"❌ Fichier manquant : {e}")
        return

    print("✅ Fichiers chargés avec succès !")

    # Harmonisation des noms des colonnes
    df_covid = df_covid.rename(columns={"Country": "Country"})
    df_vaccine = df_vaccine.rename(columns={"Country": "Country"})

    # Supprimer la colonne "date" inutile
    df_vaccine = df_vaccine.drop(columns=["date"], errors="ignore")

    # Fusionner sur la colonne "Country"
    df_merged = pd.merge(df_covid, df_vaccine, on="Country", how="inner")

    # Supprimer les valeurs manquantes
    df_merged = df_merged.dropna()

    # Convertir les valeurs numériques
    df_merged["Cases"] = pd.to_numeric(df_merged["Cases"], errors="coerce")
    df_merged["Deaths"] = pd.to_numeric(df_merged["Deaths"], errors="coerce")
    df_merged["Recovered"] = pd.to_numeric(df_merged["Recovered"], errors="coerce")
    df_merged["Total_Vaccinations"] = pd.to_numeric(df_merged["Total_Vaccinations"], errors="coerce")
    df_merged["Vaccinated_Percent"] = pd.to_numeric(df_merged["Vaccinated_Percent"], errors="coerce")

    # Supprimer les anciennes données avant d'enregistrer
    if os.path.exists(merged_data_path):
        os.remove(merged_data_path)

    # Sauvegarder le dataset enrichi
    df_merged.to_csv(merged_data_path, index=False)

    print("\n✅ Fusion terminée ! Données enregistrées dans 'data/covid_vaccine_data.csv'")
    print("\n🔎 Vérification des 10 premières lignes :")
    print(df_merged.head(10))

# Exécuter la fusion
merge_datasets()
