"""
Script de suppression de tarifs Atelier 12
=========================================
Ce script permet de supprimer automatiquement les tarifs associés à des produits
Atelier 12 en fonction d'une référence de produit donnée.

Il utilise l'API de l'Imprimerie Européenne pour :
1. Récupérer la liste des produits correspondant à une référence
2. Pour chaque produit, récupérer tous les tarifs associés
3. Supprimer chaque tarif individuellement

Auteur: [Fabrice Thiébaut]
"""

import requests
import sys
from login_ing import get_login

# =============================================================================
# AUTHENTIFICATION
# =============================================================================
# Récupération des headers d'authentification via le module login_ing
# Ces headers contiennent le token d'accès nécessaire pour les appels API
headers = get_login()

# Vérification que l'authentification a réussi
if headers is None:
    input("Problème de login")
    sys.exit()

# =============================================================================
# CONFIGURATION DE LA RECHERCHE
# =============================================================================
# Définition du préfixe de référence à rechercher
# Les produits dont la référence commence par cette chaîne seront traités
nouvelle_reference = "BRCAL"

# Code commenté pour permettre une saisie interactive de la référence
# nouvelle_reference = input("Entrez le début de la référence, 5 caractères mini : ")
# if len(nouvelle_reference < 5:
#     print("Pas assez de caractère !")
#     input("Appuyez sur Entrée pour fermer la console...")
#     sys.exit()

# =============================================================================
# RÉCUPÉRATION DES PRODUITS
# =============================================================================
# Construction de l'URL pour rechercher les produits Atelier 12
# - order=set_id : tri par identifiant de set
# - search : filtre sur la référence
url_product = f"https://api.imprimerie-europeenne.com/v1/workshop/exaprint-products?&order=set_id&search={nouvelle_reference}"

# Appel API pour récupérer la liste des produits
response_product = requests.get(url_product, headers=headers)

# Vérification du succès de la requête
if response_product.status_code != 200:
    print("Impossible de récupérer la liste de produit.")
    input("Appuyez sur Entrée pour fermer la console...")
    sys.exit()

# =============================================================================
# TRAITEMENT DES PRODUITS ET SUPPRESSION DES TARIFS
# =============================================================================
# Vérification qu'au moins un produit a été trouvé
elif len(response_product.json()['data']) > 0:
    # Extraction de la liste des produits depuis la réponse JSON
    products = response_product.json()['data']
    
    # Liste pour stocker les références des produits (non utilisée actuellement)
    product_list_references = []
    
    # Parcours de chaque produit trouvé
    for product in products:
        # Encodage du set_id pour l'URL :
        # - "+" devient "%2B" (encodage URL du caractère +)
        # - " " (espace) devient "+" (encodage URL standard des espaces)
        set_id = product['set_id'].replace("+", "%2B").replace(" ", "+")
        
        # Construction de l'URL pour récupérer les tarifs du produit
        # - contain=ExaprintProductsSize : inclut les informations de taille
        # - page=1 : première page de résultats
        # - order=quantity : tri par quantité
        # - limit=10000 : nombre maximum de résultats (pour tout récupérer)
        url_price = f"https://api.imprimerie-europeenne.com/v1/workshop/exaprint?search={set_id}&contain=ExaprintProductsSize&page=1&order=quantity&limit=10000"
        
        # Appel API pour récupérer les tarifs du produit
        response_price = requests.get(url_price, headers=headers)
        
        # Extraction des données de tarifs depuis la réponse JSON
        row_prices = response_price.json()["data"]
        
        # Vérification qu'il y a des tarifs à supprimer
        if len(row_prices) > 0:
            # Parcours de chaque tarif pour le supprimer
            for price in row_prices:
                # Récupération des informations du tarif
                id = str(price['id'])           # Identifiant unique du tarif
                set_id = price['set_id']        # Référence du produit
                quantity = price['quantity']    # Quantité associée au tarif
                
                # Construction de l'URL de suppression avec l'ID du tarif
                url_delete = f"https://api.imprimerie-europeenne.com/v1/workshop/exaprint/{id}"
                
                # Appel API DELETE pour supprimer le tarif
                response_delete = requests.delete(url_delete, headers=headers)
                
                # Vérification du résultat de la suppression
                if response_delete.status_code != 200:
                    # Échec de la suppression - affichage d'un message d'erreur
                    print(f"Impossible de supprimer le tarif. Produit : {set_id} et quantité : {quantity}")
                    # Code commenté pour arrêter le script en cas d'erreur
                    # input("Appuyez sur Entrée pour fermer la console...")
                    # sys.exit()
                else:
                    # Succès de la suppression - affichage d'un message de confirmation
                    print(f"Suppression ok : Produit : {set_id} et quantité : {quantity}")

