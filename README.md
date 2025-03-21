# Machine Learning - Predict & Test Interface

## Description
Ce projet est un outil de machine learning permettant :  
- L'entraînement d'un modèle d'intelligence artificielle (IA) sur des données de santé liées au COVID.  
- La mise à disposition d'une interface web simple avec **Flask** et un fichier `index.html`, où l'on peut tester la fiabilité du modèle directement en ligne.  

## Fonctionnalités
- Scripts Python utilisant **pandas** pour le traitement des données.  
- Entraînement de plusieurs modèles (RandomForest, XGBoost).  
- Visualisation et test des prédictions via une interface web.  

## Structure
- `fusion.py`, `add_data.py`, `scraping.py` : traitement et récupération des données.  
- `ml_covid_prediction.py`, `ml_covid_randomforest.py`, `ml_covid_xgboost.joblib` : modèles et prédiction.  
- `index.html` : page d'accueil de l'interface Flask.  
- `main.py` : lance l'application web.  

## Dépendances principales
- Python 3.x  
- Flask  
- Pandas  
- Scikit-learn  
- XGBoost  

## Lancer le projet localement
```bash
# Activer ton environnement virtuel si nécessaire

# Installer les dépendances
pip install pandas flask scikit-learn xgboost  

# Lancer l'application
python main.py
