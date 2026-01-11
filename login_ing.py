"""
Module d'authentification pour l'API Imprimerie Européenne.

Ce module permet de récupérer un token Bearer d'authentification en utilisant
les identifiants stockés dans un fichier de configuration externe.
"""

import os
import sys
import requests
import json


def get_login():
    """
    Authentifie l'utilisateur auprès de l'API Imprimerie Européenne et retourne les headers d'authentification.
    
    Cette fonction :
    1. Charge les identifiants depuis le fichier 'config.data'
    2. Effectue une requête POST pour obtenir un token Bearer
    3. Retourne les headers HTTP contenant le token pour les requêtes ultérieures
    
    Returns:
        dict: Dictionnaire contenant les headers d'authentification avec :
            - 'x-api-key': La clé API
            - 'Authorization': Le token Bearer
        None: Si l'authentification échoue ou si le fichier de config est introuvable
    """
    # Chargement des paramètres de configuration à partir d'un fichier externe
    if os.path.exists('config.data'):
        with open('config.data', 'r') as file:
            for line in file:
                # Ignorer les lignes commentées (commençant par #)
                if not line.startswith('#'):
                    # Parser chaque ligne au format "clé=valeur"
                    key, value = line.strip().split('=')
                    if key == 'login':
                        login = value
                    elif key == 'password':
                        password = value
                    elif key == 'your_api_key':
                        your_api_key = value
    else:
        print("Le fichier de configuration n'a pas été trouvé.")
        sys.exit()
    
    # Initialisation des variables pour le token et les headers
    bearer_token = ""
    headers = {}
    
    # URL de l'endpoint d'authentification de l'API
    url_token = "https://api.imprimerie-europeenne.com/v1/backend/authentication/login"
    
    # Envoi de la requête POST pour récupérer le token de connexion
    # Le header 'x-api-key' est requis pour l'authentification
    response_token = requests.post(
        url_token, 
        json={"username": login, "password": password}, 
        headers={'x-api-key': your_api_key}
    )
    
    # Vérification du statut de la réponse
    if response_token.status_code != 200:
        print("Impossible de récupérer le token Bearer.")
        headers = {}
        # En cas d'échec, retourner None plutôt que de quitter le programme
        # pour permettre une gestion d'erreur plus flexible
        return None
    else:
        # Extraction du token depuis la réponse JSON
        bearer_token = response_token.json()['token']
        
        # Construction des headers d'authentification pour les requêtes suivantes
        headers = {
            'x-api-key': your_api_key,
            'Authorization': f'Bearer {bearer_token}'
        }
        return headers