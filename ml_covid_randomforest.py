import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import xgboost as xgb

# 1. Charger les données enrichies
data = pd.read_csv("data/covid_vaccine_data.csv")
data = data.dropna()

# 2. Sélectionner les variables d'entrée et la cible
X = data[["Cases", "Vaccinated_Percent", "Total_Vaccinations"]]
y = data["Deaths"]

# 3. Division en jeux d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Entraîner un modèle XGBoost avec contrainte pour éviter les valeurs négatives
model = xgb.XGBRegressor(
    n_estimators=1500,
    max_depth=20,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.8,
    random_state=42,
    base_score=0,
    objective='reg:squarederror'  # Assure une régression sans valeur aberrante
)
model.fit(X_train, y_train)

# 5. Évaluer le modèle
y_pred = model.predict(X_test)
y_pred = np.clip(y_pred, 0, None)  # Évite les prédictions négatives
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"✅ Modèle XGBoost entraîné avec succès")
print(f"R² : {r2:.4f}")
print(f"RMSE : {rmse:.2f}")

# 6. Enregistrer le modèle entraîné
joblib.dump(model, "ml_covid_xgboost.joblib")
print("✅ Modèle sauvegardé sous ml_covid_xgboost.joblib")
