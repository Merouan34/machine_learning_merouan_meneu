import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# 1. Charger les données enrichies
data = pd.read_csv("data/covid_vaccine_data.csv")

# 2. Préparer les données (suppression des valeurs manquantes)
data = data.dropna()

# 3. Sélectionner les features (variables d'entrée) et la target (variable à prédire)
X = data[["Cases", "Vaccinated_Percent", "Total_Vaccinations"]]
y = data["Deaths"]

# 4. Séparer en jeux d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Entraîner le modèle de régression linéaire
model = LinearRegression()
model.fit(X_train, y_train)

# 6. Faire des prédictions
y_pred = model.predict(X_test)

# 7. Évaluer le modèle
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"\n✅ Modèle entraîné avec succès !")
print(f"R² : {r2:.4f}")
print(f"RMSE : {rmse:.2f}\n")

# 8. Visualiser la comparaison prédiction vs réel
plt.scatter(y_test, y_pred)
plt.xlabel("Valeurs réelles (décès)")
plt.ylabel("Prédictions (décès)")
plt.title("Prédiction du nombre de décès vs valeurs réelles")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.show()

# 9. Fonction de prédiction personnalisée
def predict_for_country(cases, vaccinated_percent, total_vaccinations):
    data_point = np.array([[cases, vaccinated_percent, total_vaccinations]])
    prediction = model.predict(data_point)[0]
    print(f"\nPour {cases} cas, un taux de vaccination de {vaccinated_percent}% et {total_vaccinations} doses administrées,")
    print(f"le modèle prédit environ {int(prediction):,} décès.")

# Exemple d'utilisation
# predict_for_country(1000000, 75, 5000000)
