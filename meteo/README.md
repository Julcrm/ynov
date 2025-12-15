# Application Météo Console

## Introduction

Ce projet est une application console Python permettant de consulter les données météorologiques en temps réel des stations de Toulouse Métropole.

L'application interroge d'une API pour récupérer un catalogue de stations, permet à l'utilisateur de naviguer, de filtrer les résultats par ville, et d'afficher les relevés météorologiques (température, humidité, pression).

---

## Fonctionnalités Principales

*   **Catalogue de Stations** : Chargement et structuration automatique des données depuis l'API de Toulouse Métropole.
*   **Navigation Interactive** : Interface console avancée (basée sur `rich` et `questionary`) permettant de sélectionner une ville puis une station.
*   **Visualisation des Données** : Affichage clair des derniers relevés météorologiques.
*   **Parcours Séquentiel** : Navigation entre les stations d'une même ville.

---

## Architecture Technique

Le projet respecte le principe de responsabilité unique (SRP) et est structuré en couches logiques distinctes :

*   **Loaders** : Responsables de la communication avec l'API et du chargement brut des données.
*   **Models** : Définition des objets (`City`, `Station`) et de la configuration.
*   **Filters** : Ensemble de classes permettant le tri, le nettoyage et la sélection des données (Pattern Composite).
*   **Services** : Couche de coordination (Façade) simplifiant l'accès aux données pour l'orchestrateur.
*   **Orchestrator** : Contrôleur principal.
*   **UI** : Gère exclusivement l'affichage et les interactions utilisateur.

### Design Patterns Implémentés

Pour assurer la maintenabilité et l'extensibilité du code, les patrons de conception suivants ont été intégrés :

1.  **Singleton** (`models/configuration.py`) : 
    Assure l'unicité de l'instance de configuration à travers toute l'application, optimisant le chargement des paramètres depuis `config.json`.

2.  **Factory** (`factories/station_navigator_factory.py`) : 
    Encapsule la logique de création et de tri des navigateurs de stations.

3.  **Command** (`commands/`) : 
    Gère les interactions utilisateur (Navigation, Quitter, Redémarrer) sous forme d'objets encapsulés, remplaçant les structures conditionnelles complexes dans l'orchestrateur.

4.  **Composite** (`filters/composite_filter.py`) : 
    Permet de traiter une séquence de filtres comme un filtre unique, facilitant la création de pipelines de traitement de données.

---

## Installation et Exécution

### Prérequis
*   Python 3.10 ou version ultérieure.

### Procédure

1.  **Cloner le dépôt** et accéder au répertoire :
    ```bash
    git clone https://github.com/Julcrm/ynov.git
    cd ynov
    ```

2.  **Installer les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

3.  **Lancer l'application** :
    ```bash
    python -m meteo
    ```

---

## Utilisation avec Docker 🐳

Si vous préférez ne pas installer de dépendances sur votre machine, vous pouvez utiliser Docker.

1.  **Construire l'image** (depuis la racine du projet) :
    ```bash
    docker build -t app-meteo -f meteo/Dockerfile .
    ```

2.  **Lancer conteneur** :
    ```bash
    docker run -it --rm app-meteo
    ```

---

## Configuration

Le comportement de l'application est paramétrable via le fichier `meteo/config.json`. Ce fichier centralise :
*   Les URLs de l'API.
*   Les mappages de colonnes pour les DataFrames.
*   Les critères de filtrage par défaut.

---

## Structure du Projet

```
meteo/
├── __main__.py             # Point d'entrée de l'application
├── config.json             # Fichier de configuration
│
├── commands/               # Implémentation du pattern Command
├── interfaces/             # Interfaces abstraites du système
├── loaders/                # Modules de chargement de données
├── filters/                # Logique de filtrage (Composite)
├── extractors/             # Extraction de métadonnées
├── models/                 # Objets métiers et Singleton Configuration
├── factories/              # Fabriques d'objets
├── services/               # Services métiers
├── ui/                     # Interface utilisateur console
└── orchestrator/           # Gestionnaire de workflow
```
