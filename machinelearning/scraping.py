import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# User-Agent pour éviter le blocage
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_covid_data(country, url):
    """Scrape les statistiques COVID pour un pays donné en gérant les erreurs"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️ Erreur pour {country} ({url}) : {e}")
        return [country, "N/A", "N/A", "N/A"]

    time.sleep(1)  # Pause pour éviter le blocage

    soup = BeautifulSoup(response.text, 'html.parser')

    # Récupérer les statistiques principales
    stats = soup.find_all("div", class_="maincounter-number")
    if stats and len(stats) >= 3:
        cases = stats[0].text.strip().replace(",", "")
        deaths = stats[1].text.strip().replace(",", "")
        recovered = stats[2].text.strip().replace(",", "")
        return [country, cases, deaths, recovered]
    else:
        print(f"⚠️ Pas assez de données pour {country}")
        return [country, "N/A", "N/A", "N/A"]

def scrape_all_countries():
    """Scrape les données COVID à partir des URLs du fichier CSV"""
    try:
        df = pd.read_csv("data/country_urls.csv")
    except FileNotFoundError:
        print("❌ Fichier 'data/country_urls.csv' introuvable. Exécute d'abord le script de génération d'URLs.")
        return

    # Vérifier les premières URLs générées
    print("\n🔎 Exemple d'URLs utilisées :")
    for i, row in df.iterrows():
        print(f"🌍 {row['Country']} → {row['URL']}")
        if i == 5:
            break

    # Liste pour stocker les données
    data = []
    
    print(f"\n🔄 Scraping de {len(df)} pays...\n")
    for _, row in df.iterrows():
        country, url = row["Country"], row["URL"]
        print(f"📡 Scraping {country} ({url})...")
        result = scrape_covid_data(country, url)
        data.append(result)

    # Supprime l'ancien fichier avant d'enregistrer le nouveau
    if os.path.exists("data/covid_data_all_countries.csv"):
        os.remove("data/covid_data_all_countries.csv")

    # Sauvegarde dans un fichier CSV
    df_out = pd.DataFrame(data, columns=["Country", "Cases", "Deaths", "Recovered"])
    df_out.to_csv("data/covid_data_all_countries.csv", index=False)

    print("\n✅ Scraping terminé ! Données enregistrées dans data/covid_data_all_countries.csv")

# Exécuter le scraping
scrape_all_countries()

