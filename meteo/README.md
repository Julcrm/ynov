# Application Météo Console

## Description

Cette application console permet à un utilisateur de consulter les données météorologiques de différentes stations à Toulouse et ses environs. L'application charge un catalogue de stations météo depuis l'API open-data de Toulouse Métropole, puis guide l'utilisateur à travers un processus de sélection pour choisir une ville et une station spécifique. Enfin, elle affiche les dernières données disponibles pour cette station (température, humidité, pression).

L'application utilise une architecture en couches avec des design patterns (Factory, Composite, Façade) et une structure de données doublement chaînée pour la navigation entre les stations.

---

## Structure du Projet

```
git/
├── .venv/                    # Environnement virtuel Python
├── requirements.txt          # Dépendances du projet
└── meteo/                    # Package principal de l'application
    ├── __init__.py
    ├── __main__.py           # Point d'entrée de l'application
    ├── config.json           # Configuration (URLs, colonnes, filtres)
    ├── config_loader.py      # Utilitaire de chargement de config
    │
    ├── interfaces/           # Définition des contrats/interfaces
    │   ├── __init__.py
    │   ├── base_interfaces.py
    │   └── navigation_interface.py
    │
    ├── loaders/              # Chargement des données depuis les APIs
    │   ├── __init__.py
    │   ├── cities_loader.py
    │   └── station_data_loader.py
    │
    ├── filters/              # Filtrage des DataFrames
    │   ├── __init__.py
    │   ├── city_filter.py
    │   ├── keyword_filter.py
    │   ├── column_filter.py
    │   └── composite_filter.py
    │
    ├── extractors/           # Extraction de données spécifiques
    │   ├── __init__.py
    │   └── data_extractor.py
    │
    ├── models/               # Structures de données
    │   ├── __init__.py
    │   ├── city.py
    │   ├── station.py
    │   └── station_node.py
    │
    ├── factories/            # Création d'objets complexes
    │   ├── __init__.py
    │   └── station_navigator_factory.py
    │
    ├── services/             # Logique métier et coordination
    │   ├── __init__.py
    │   ├── weather_data_service.py
    │   ├── user_selection_service.py
    │   └── station_linked_list.py
    │
    ├── ui/                   # Interface utilisateur console
    │   ├── __init__.py
    │   └── interactive_ui.py
    │
    └── orchestrator/         # Orchestration du workflow
        ├── __init__.py
        └── weather_station_orchestrator.py
```

---

## Installation

Pour faire fonctionner ce projet, vous aurez besoin de Python 3.10+ et de quelques dépendances.

### 1. Clonez le projet
```bash
git clone https://github.com/Julcrm/ynov.git
cd git
```

### 2. Créez un environnement virtuel
Ceci permet d'isoler les dépendances du projet et d'éviter les conflits.
```bash
python3 -m venv .venv
```

### 3. Activez l'environnement virtuel
*   Sur macOS / Linux :
    ```bash
    source .venv/bin/activate
    ```
*   Sur Windows :
    ```bash
    .venv\Scripts\activate
    ```

### 4. Installez les dépendances
Cette commande installe `pandas`, `requests`, `questionary` et `rich` (et leurs dépendances) dans votre environnement isolé.
```bash
pip install -r requirements.txt
```

---

## Utilisation

Une fois l'installation terminée et l'environnement virtuel activé, lancez l'application en tant que module Python depuis la racine du projet :

```bash
python -m meteo
```

Suivez ensuite les instructions qui s'affichent dans la console pour :
1. Sélectionner une ville parmi celles disponibles
2. Choisir une station météo pour cette ville
3. Consulter les données météorologiques
4. Naviguer entre les stations (précédente/suivante)

---

## Architecture et Composants

### Point d'entrée

*   `__main__.py` : **Point d'entrée de l'application**. Configure tous les composants via injection de dépendances, charge la configuration depuis `config.json`, et lance l'orchestrateur.
*   `config.json` : **Fichier de configuration central** au format JSON. Contient les URLs des APIs, les noms de colonnes, et les critères de filtrage.
*   `config_loader.py` : Module utilitaire pour charger automatiquement le fichier `config.json` depuis le dossier du package.
*   `requirements.txt` : Liste les dépendances Python nécessaires au projet.

### `interfaces/`

*   `base_interfaces.py` : Définit les **interfaces de base** (DataLoader, DataFilter, UserInterface, etc.) que les composants concrets doivent implémenter.
*   `navigation_interface.py` : Définit l'interface `StationNavigator` pour la navigation bidirectionnelle entre stations.

### `loaders/`

*   `cities_loader.py` : Charge le **catalogue complet** des stations depuis l'API CSV de Toulouse Métropole.
*   `station_data_loader.py` : Charge les **données spécifiques** (température, humidité, etc.) pour une station donnée depuis l'API JSON.

### `filters/`

*   `city_filter.py` : Filtre un DataFrame pour ne conserver que les stations d'une ville spécifique.
*   `keyword_filter.py` : Filtre basé sur la présence/absence de mots-clés dans une colonne.
*   `column_filter.py` : Sélectionne un sous-ensemble de colonnes dans un DataFrame.
*   `composite_filter.py` : Implémente le **pattern Composite** pour enchaîner plusieurs filtres séquentiellement.

### `extractors/`

*   `data_extractor.py` : Extrait des informations spécifiques d'un DataFrame (villes uniques, stations uniques, etc.) en utilisant un tri naturel.

### `models/`

*   `city.py` : Modèle de données représentant une ville.
*   `station.py` : Modèle de données représentant une station météo avec son ID et sa ville.
*   `station_node.py` : Nœud d'une liste doublement chaînée contenant une station et des références vers les nœuds adjacents.

### `factories/`

*   `station_navigator_factory.py` : Implémente le **pattern Factory** pour créer des navigateurs de stations à partir d'une liste. Gère le tri automatique des stations.

### `services/`

*   `weather_data_service.py` : **Service Façade** qui coordonne les loaders, filtres et extracteurs. Gère le cache du catalogue et fournit une API simplifiée.
*   `user_selection_service.py` : Service de haut niveau pour gérer les sélections utilisateur via l'UI.
*   `station_linked_list.py` : Implémente une **liste doublement chaînée** pour naviguer entre les stations (next, previous, reset, position).

### `ui/`

*   `interactive_ui.py` : Interface utilisateur conversationnelle pour la console. Utilise `rich` pour l'affichage stylisé et `questionary` pour les menus interactifs au clavier.

### `orchestrator/`

*   `weather_station_orchestrator.py` : **Orchestrateur principal** qui coordonne le workflow complet de l'application. Gère les erreurs et le flux d'exécution en appelant les services dans le bon ordre.

---

## Technologies Utilisées

- **Python 3.10+** : Langage de programmation
- **pandas** : Manipulation et analyse de données
- **requests** : Requêtes HTTP vers les APIs
- **rich** : Affichage console stylisé avec tableaux et couleurs
- **questionary** : Menus interactifs navigables au clavier

---

## Configuration

Le fichier `config.json` permet de configurer :
- Les URLs des APIs Toulouse Métropole
- Les noms des colonnes dans les DataFrames
- Les mots-clés de filtrage
- Les colonnes à afficher dans les résultats

