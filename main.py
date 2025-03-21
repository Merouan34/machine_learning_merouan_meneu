from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib

# Charger le modèle préalablement entraîné
model = joblib.load("ml_covid_xgboost.joblib")

# Créer l'application Flask
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    cases = float(request.form['cases'])
    vaccinated_percent = float(request.form['vaccinated_percent'])
    total_vaccinations = float(request.form['total_vaccinations'])

    prediction = model.predict(np.array([[cases, vaccinated_percent, total_vaccinations]]))[0]

    return render_template('index.html', prediction_text=f"Prédiction du nombre de décès : {int(prediction):,}")

if __name__ == '__main__':
    app.run(debug=True)
