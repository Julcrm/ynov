import json
import os
from typing import Dict, Any

def load_config(path: str = None) -> Dict[str, Any]:
    """
    Charge la configuration depuis un fichier JSON.

    Args:
        path (str): Le chemin vers le fichier de configuration.
                   Par défaut, cherche config.json dans le même dossier que ce fichier.

    Returns:
        Dict[str, Any]: Un dictionnaire contenant la configuration.
    """
    if path is None:
        # Obtenir le chemin du dossier contenant ce fichier
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "config.json")

    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erreur : Le fichier de configuration '{path}' est introuvable.")
        exit(1) # Quitte le programme si la config est absente
    except json.JSONDecodeError as e:
        print(f"Erreur lors de la lecture du fichier de configuration : {e}")
        exit(1)