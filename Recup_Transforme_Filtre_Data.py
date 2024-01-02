"""
Created on Sat Dec 23 02:11:32 2023

@author: naima abdoune 
"""

import requests
import re
import time
from datetime import datetime
import pandas as pd
from nltk.corpus import stopwords
# Liste des stopwords pour le français
stop_words = set(stopwords.words("french"))


###################################    Extraction des données   ######################################
# URL de l'API
api_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=20"

# Renommer les noms des colonnes
column_mapping = {
    "stationcode": "Identifiant station",
    "name": "Nom station",
    "is_installed": "Station en fonctionnement",
    "capacity": "Capacité de la station",
    "numdocksavailable": "Nombre bornettes libres",
    "numbikesavailable": "Nombre total vélos disponibles",
    "mechanical": "Vélos mécaniques disponibles",
    "ebike": "Vélos électriques disponibles",
    "is_renting": "Borne de paiement disponible",
    "is_returning": "Retour vélib possible",
    "duedate": "Actualisation de la donnée",
    "coordonnees_geo": "Coordonnées géographiques",
    "nom_arrondissement_communes": "Nom communes équipées",
    "code_insee_commune": "Code INSEE communes équipées"
}

# Fonction pour effectuer une requête à l'API
def fetch_data():
    try:
        response = requests.get(api_url)
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        print(f"Erreur lors de la requête à l'API : {e}")
        return []

# Fonction pour écrire les données dans un fichier CSV
def write_to_csv(data, filename="velib_data.csv"):
    if not data:
        print("Aucune donnée à écrire.")
        return

    # Transformer les noms de colonnes
    transformed_data = [{column_mapping.get(key, key): value for key, value in entry.items()} for entry in data]
       
    
############################ Nettoyage et filtrage des données ########################################

    # Créer un DataFrame à partir des données transformées
    df = pd.DataFrame(transformed_data)
    
    # Supprimer la colonne 'Code INSEE communes équipées' (si elle existe)
    df = df.drop(columns=['Code INSEE communes équipées'.strip()])

    
    # Supprimer les lignes vides
    # On ne peut pas supprimer les lignes vides en premier avant de supprimer la colonne vide 'Code INSEE communes équipées'
    #car si on commence à supprimer les lignes vides, cela supprime toutes les lignes, car toutes les lignes contiennent 
    #un champ 'Code INSEE communes équipées' vide 
    df = df.dropna()

     
    #supprimer alphanumérique en numérique au niveau de identifiant station, 
    #supprimer alphanumérique en numérique au niveau de capacité de la station,
    #supprimer alphanumérique en numérique au niveau de nombre bronettes libres, 
    #supprimer alphanumérique en numérique au niveau de nombres total vélos  disponibles, 
    #supprimer alphanumérique en numérique au niveau de nombres Vélos mécaniques disponibles, 
    #supprimer alphanumérique en numérique au niveau de nombres Vélos électriques disponibles, 


    df["Identifiant station"] = df["Identifiant station"].apply(lambda x: re.sub(r'\D', '', str(x)))
    df["Capacité de la station"] = df["Capacité de la station"].apply(lambda x: re.sub(r'\D', '', str(x)))
    df["Nombre bornettes libres"] = df["Nombre bornettes libres"].apply(lambda x: re.sub(r'\D', '', str(x)))
    df["Nombre total vélos disponibles"] = df["Nombre total vélos disponibles"].apply(lambda x: re.sub(r'\D', '', str(x)))
    df["Vélos mécaniques disponibles"] = df["Vélos mécaniques disponibles"].apply(lambda x: re.sub(r'\D', '', str(x)))
    df["Vélos électriques disponibles"] = df["Vélos électriques disponibles"].apply(lambda x: re.sub(r'\D', '', str(x)))

    
    
    
    # Vérifier et corriger le format du noms des stations et noms des communes
    def formatter_nom(nom):
        if pd.isna(nom):
            return nom

        mots = re.split(r'([\s-])', nom)
        mots_formates = [
            mot.lower() if mot.lower() in stop_words else mot.capitalize()
            for mot in mots
        ]
        return ''.join(mots_formates)
    
    # Appliquer la fonction de formatage sur la colonne 'Nom station' et 'Nom communes équipées'
    df['Nom station'] = df['Nom station'].apply(formatter_nom)
    df['Nom communes équipées'] = df['Nom communes équipées'].apply(formatter_nom)
    
    
    
    # Filtrer les lignes où 'Station en fonctionnement','Borne de paiement disponible' et 'Retour vélib possible' ne sont pas 'OUI' ou 'NON'
    df = df[df['Station en fonctionnement'].str.upper().isin(['OUI', 'NON']) | df['Station en fonctionnement'].isna()]
    df = df[df['Retour vélib possible'].str.upper().isin(['OUI', 'NON']) | df['Retour vélib possible'].isna()]
    df = df[df['Borne de paiement disponible'].str.upper().isin(['OUI', 'NON']) | df['Borne de paiement disponible'].isna()]

        
    # Écrire les données dans un fichier CSV
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        # Écrire l'en-tête du fichier CSV s'il est vide
        if file.tell() == 0:
            df.to_csv(file, header=True, index=False)
        else:
            df.to_csv(file, header=False, index=False)



######################## Extraction des données chaque 4 minutes ###############################
# Boucle principale pour récupérer les données toutes les 4 minutes
while True:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Chargement des données à {current_time}...")
    
    # Récupérer les données depuis l'API
    api_data = fetch_data()

    # Écrire les données dans un fichier CSV avec les colonnes renommées et les filtres appliqués
    write_to_csv(api_data)

    print("Données chargées avec succès. Attente de 4 minutes avant la prochaine requête...")
    time.sleep(240)  # Attendre 4 minutes (240 secondes)
