import json
from typing import Dict, Any

def load_config(path: str = "config.json") -> Dict[str, Any]:
    """
    Charge la configuration depuis un fichier JSON.

    Args:
        path (str): Le chemin vers le fichier de configuration.

    Returns:
        Dict[str, Any]: Un dictionnaire contenant la configuration.
    """
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erreur : Le fichier de configuration '{path}' est introuvable.")
        exit(1) # Quitte le programme si la config est absente
    except json.JSONDecodeError as e:
        print(f"Erreur lors de la lecture du fichier de configuration : {e}")
        exit(1)