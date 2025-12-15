
from typing import Any

class Configuration:
    """
    Classe Singleton gérant la configuration globale de l'application.
    Assure qu'une seule instance de la configuration existe en mémoire.
    """
    _instance = None

    def __new__(cls):
        """
        Crée ou retourne l'instance unique de Configuration.
        Initialise le dictionnaire de configuration interne si c'est la première création.
        """
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
            cls._instance._config = {}
        return cls._instance

    def set_value(self, key: str, value: Any):
        """
        Définit une valeur de configuration pour une clé donnée.

        Args:
            key (str): La clé de configuration.
            value (Any): La valeur à stocker.
        """
        self._config[key] = value

    def get_value(self, key: str) -> Any:
        """
        Récupère une valeur de configuration par sa clé.

        Args:
            key (str): La clé à rechercher.

        Returns:
            Any: La valeur associée à la clé, ou None si la clé n'existe pas.
        """
        return self._config.get(key, None)
