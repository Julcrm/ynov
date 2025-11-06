"""Modèle de données pour une ville."""

class City:
    """Représente une ville avec ses attributs."""
    def __init__(self, name: str):
        """
        Initialise un objet City.

        Args:
           - name (str): Le nom de la ville.
        """
        self.name = name

    def __str__(self) -> str:
        """
        Retourne la représentation de la ville sous forme de chaîne de caractères
        destinée à l'utilisateur.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Retourne la représentation de l'objet City.
        """
        return f"City(name='{self.name}')"