import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URL principale du site Worldometer
URL = "https://www.worldometers.info/coronavirus/"

# User-Agent pour éviter le blocage
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Liste des noms de continents et autres entrées à exclure
EXCLUDED_ENTITIES = ["World", "Asia", "Europe", "North America", "South America", "Oceania", "Africa", "Total",
                     "MS Zaandam", "Diamond Princess"]

def get_country_urls():
    """Récupère la liste des pays et leurs liens en FORÇANT le format correct."""
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Erreur de connexion : {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    country_links = []
    table = soup.find("table", id="main_table_countries_today")

    if table:
        for row in table.find("tbody").find_all("tr"):
            columns = row.find_all("td")
            if columns and len(columns) > 1:
                country_name = columns[1].text.strip()

                # Exclure les continents et entrées non pertinentes
                if country_name in EXCLUDED_ENTITIES or len(country_name) < 2:
                    continue

                # ✅ FORCER le bon format d'URL
                country_slug = country_name.lower().replace(" ", "-").replace(".", "").replace(",", "").replace("(", "").replace(")", "").replace("’", "").replace("'", "")
                country_url = f"https://www.worldometers.info/coronavirus/country/{country_slug}/"

                country_links.append([country_name, country_url])

    # ✅ Supprime l'ancien fichier avant d'écrire les nouvelles données
    if os.path.exists("data/country_urls.csv"):
        os.remove("data/country_urls.csv")

    # ✅ Enregistrement des URLs dans un fichier CSV
    df = pd.DataFrame(country_links, columns=["Country", "URL"])
    df.to_csv("data/country_urls.csv", index=False)
    print("\n✅ Fichier 'data/country_urls.csv' généré avec succès !")

    # ✅ Vérification des 10 premières URLs générées
    print("\n🔎 Vérification des 10 premières URLs :")
    for i in range(min(10, len(country_links))):
        print(f"🌍 {country_links[i][0]} → {country_links[i][1]}")

# ✅ Exécuter la récupération des URLs
get_country_urls()
