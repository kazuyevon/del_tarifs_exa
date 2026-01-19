# Automatisation API : Suppression Massive de Tarifs (Exaprint)

Ce script Python a été conçu pour résoudre une problématique concrète de gestion de catalogue dans le secteur de l'imprimerie. Il permet d'automatiser la suppression de tarifs obsolètes via l'API de l'Imprimerie Européenne.

## 🎯 Problématique Métier
La mise à jour des tarifs automatique via API fonctionne parfaitement mais parfois à cause de délai changeant (on stocke les délais avec les traifs associés), des tarifs obsolètes restaient stockés et la suppression pour des centaines de références est une tâche chronophage et sujette aux erreurs. Ce script permet de cibler une famille de produits (via une référence de base) et de purger l'intégralité des tarifs associés en quelques secondes.

## 🛠️ Fonctionnalités techniques
* **Authentification sécurisée :** Utilisation d'un module d'authentification tiers (`login_ing`) pour la gestion des tokens.
* **Recherche par pattern :** Filtrage dynamique des produits basés sur un préfixe de référence (ex: `BRCAL`).
* **Traitement de données imbriquées :** 1. Récupération de la liste des produits.
    2. Parsing des `set_id` avec gestion de l'encodage URL (remplacement des caractères spéciaux).
    3. Boucle de suppression sur les tarifs associés.
* **Gestion des erreurs :** Vérification des codes de statut HTTP (200, etc.) pour assurer l'intégrité du processus.

## 🚀 Technologies utilisées
* **Python 3**
* **Bibliothèque Requests :** Pour les appels API REST.
* **API REST :** Interaction avec les endpoints Workshop de l'Imprimerie Européenne.

## 📋 Prérequis et Installation
1. **Configuration :** Le script s'appuie sur un fichier `config.data` (non inclus pour des raisons de sécurité) qui contient les paramètres de connexion.
2. **Authentification :** Le module `login_ing.py` assure la liaison entre les données de configuration et l'API de l'Imprimerie Européenne.
3. **Dépendances :** `pip install requests`

## 💡 Exemple d'utilisation
Le script est configuré par défaut pour traiter les références commençant par `BRCAL`. 
Une fois lancé, il affiche en temps réel le statut de chaque suppression :
`Suppression ok : Produit : BRCAL_10x15 et quantité : 500`
