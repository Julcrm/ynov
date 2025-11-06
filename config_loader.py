import yaml
from typing import Dict, Any

def load_config(path: str = "config.yaml") -> Dict[str, Any]:
    """
    Charge la configuration depuis un fichier YAML.

    Args:
        path (str): Le chemin vers le fichier de configuration.

    Returns:
        Dict[str, Any]: Un dictionnaire contenant la configuration.
    """
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Erreur : Le fichier de configuration '{path}' est introuvable.")
        exit(1) # Quitte le programme si la config est absente
    except yaml.YAMLError as e:
        print(f"Erreur lors de la lecture du fichier de configuration : {e}")
        exit(1)