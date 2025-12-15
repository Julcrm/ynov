import json
import os
from .models.configuration import Configuration


def load_config(path: str = None):
    """
    Charge la configuration depuis un fichier JSON dans le Singleton Configuration.
    Si la configuration est déjà chargée, la retourne directement.

    Args:
        path (str): Le chemin vers le fichier de configuration.
                   Par défaut, cherche config.json dans le même dossier que ce fichier.

    Returns:
        Dict[str, Any]: Un dictionnaire contenant la configuration.
    """
    config = Configuration()

    # Si la config est déjà chargée (non vide), on la retourne
    if config._config:
        return config._config

    if path is None:
        # Obtenir le chemin du dossier contenant ce fichier
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "config.json")

    try:
        with open(path, 'r') as f:
            data = json.load(f)
            # Utilisation de set_value pour chaque élément
            for key, value in data.items():
                config.set_value(key, value)
            return config._config
    except FileNotFoundError:
        print(f"Erreur : Le fichier de configuration '{path}' est introuvable.")
        exit(1) # Quitte le programme si la config est absente
    except json.JSONDecodeError as e:
        print(f"Erreur lors de la lecture du fichier de configuration : {e}")
        exit(1)