import pandas as pd

# Charger le CSV complet des âges moyens depuis le fichier fourni
df = pd.read_csv("data/median_age.csv")  # fichier complet avec de nombreuses colonnes

# Extraire uniquement les colonnes nécessaires (pays et âge moyen)
age_data = df[['Country', 'Âge moyen']].dropna()
age_data.rename(columns={'Âge moyen': 'Median_Age'}, inplace=True)

# Charger la liste des pays depuis ton fichier principal pour comparer
covid_data = pd.read_csv("data/covid_vaccine_data.csv")

# Comparer les noms de pays
covid_countries = set(covid_data['Country'].unique())
age_countries = set(age_data['Country'].unique())

# Identifier les correspondances manquantes et les afficher
missing_in_age = covid_countries - age_countries
missing_in_covid = age_countries - covid_countries

print("✅ Pays présents dans les données Covid mais absents dans l'âge moyen :")
for country in sorted(missing_in_age):
    print(country)

print("\n✅ Pays présents dans les données d'âge mais absents dans les données Covid :")
for country in sorted(missing_in_covid):
    print(country)

# Exporter pour vérification manuelle
with open("data/countries_missing_summary.txt", "w", encoding="utf-8") as f:
    f.write("Manquants dans age_data:\n")
    f.write("\n".join(sorted(missing_in_age)))
    f.write("\n\nManquants dans covid_data:\n")
    f.write("\n".join(sorted(missing_in_covid)))

print("\n✅ Fichier de résumé généré dans data/countries_missing_summary.txt")
