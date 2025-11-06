# Application Météo Console

## Description

Cette application console permet à un utilisateur de consulter les données météorologiques de différentes stations à Toulouse et ses environs. L'application charge un catalogue de stations météo depuis l'API open-data de Toulouse Métropole, puis guide l'utilisateur à travers un processus de sélection pour choisir une ville et une station spécifique. Enfin, elle affiche les dernières données disponibles pour cette station (température, humidité, pression).

---

## Structure du Projet

```.
├── .venv/
├── main.py
├── requirements.txt
├── interfaces/
│   └── base_interfaces.py
├── loaders/
│   ├── cities_loader.py
│   └── station_data_loader.py
├── filters/
│   ├── city_filter.py
│   ├── column_filter.py
│   ├── composite_filter.py
│   └── keyword_filter.py
├── extractors/
│   └── data_extractor.py
├── ui/
│   └── interactive_ui.py
├── models/
│   ├── station.py
│   └── city.py
├── services/
│   ├── weather_data_service.py
│   └── user_selection_service.py
└── orchestrator/
    └── weather_station_orchestrator.py
```

---

## Installation

Pour faire fonctionner ce projet, vous aurez besoin de Python 3.7+ et de quelques dépendances.

1.  **Clonez le projet**
    ```bash
    git clone https://github.com/Julcrm/ynov.git
    cd git
    ```

2.  **Créez un environnement virtuel**
    Ceci permet d'isoler les dépendances du projet et d'éviter les conflits.
    ```bash
    python3 -m venv .venv
    ```

3.  **Activez l'environnement virtuel**
    *   Sur macOS / Linux :
        ```bash
        source .venv/bin/activate
        ```
    *   Sur Windows :
        ```bash
        .venv\Scripts\activate
        ```

4.  **Installez les dépendances**
    Cette commande installe `pandas`, `requests`, `PyYAML`, `questionary`et `rich` (et leurs dépendances) dans votre environnement isolé.
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

Une fois l'installation terminée et l'environnement virtuel activé, lancez simplement le script `main.py` depuis la racine du projet :

```bash
python main.py
```

Suivez ensuite les instructions qui s'affichent dans la console pour sélectionner une ville et une station météo.

---

## Description des Fichiers


*   `main.py` : **Point d'entrée de l'application**. C'est ici que toute la configuration est définie et que les objets sont créés et connectés les uns aux autres. Il lance ensuite l'orchestrateur.
*   `requirements.txt` : Liste les dépendances Python nécessaires au projet pour garantir un environnement reproductible.
*   `config.yaml` : **Fichier de configuration central**. Il externalise toutes les valeurs qui peuvent changer (URLs, noms de colonnes, etc.)
*   `config_loader.py` : Un module utilitaire simple pour lire le fichier `config.yaml` et de le transformer en dictionnaire Python utilisable par l'application.

#### `interfaces/`

*   `base_interfaces.py` : Définit les **contrats** (classes de base) que les autres composants doivent respecter.

#### `loaders/`

*   `cities_loader.py` : Responsable du chargement du **catalogue complet** des stations depuis l'API CSV.
*   `station_data_loader.py` : Responsable du chargement des **données spécifiques** (température, etc.) pour une seule station depuis l'API JSON.

#### `filters/`

*   `city_filter.py` : Filtre un DataFrame pour ne garder que les lignes correspondant à une ville donnée.
*   `keyword_filter.py` : Filtre un DataFrame en se basant sur la présence (ou l'absence) de mots-clés dans une colonne.
*   `column_filter.py` : Sélectionne un sous-ensemble de colonnes utiles dans un DataFrame.
*   `composite_filter.py` : Un filtre spécial qui permet d'**enchaîner plusieurs filtres** les uns après les autres.

#### `extractors/`

*   `data_extractor.py` : Contient la logique pour **extraire des informations spécifiques** d'un DataFrame.

#### `models/`

*   `city.py` et `station.py` : Définissent les **structures de données** de base de l'application. Ce sont des classes simples.

#### `ui/`

*   `interactive_ui.py` : Gère toutes les interactions avec l'utilisateur dans la console. Elle utilise les bibliothèques `rich` et `questionary` pour créer des menus interactifs navigables au clavier et un affichage de données stylisé.

#### `services/`

*   `weather_data_service.py` : Agit comme une **façade** pour simplifier l'accès aux données. Il coordonne les loaders, les filtres et l'extracteur.
*   `user_selection_service.py` : Gère la logique de haut niveau pour demander à un utilisateur de faire un choix dans une liste.

#### `orchestrator/`

*   `weather_station_orchestrator.py` : Le **cerveau de l'application**. Il ne fait aucun travail lui-même mais dicte le déroulement des opérations en appelant les services et l'UI dans le bon ordre.

