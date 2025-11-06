"""Modèle de données pour une station météo."""

class Station:
    """Représente une station météo avec ses informations d'identification."""

    def __init__(self, dataset_id: str, city: str):
        """
        Initialise un objet Station.

        Args:
           - dataset_id (str): L'identifiant unique de la station.
           - city (str): Le nom de la ville.
        """
        self.dataset_id = dataset_id
        self.city = city

    def __str__(self) -> str:
        """
        Retourne la représentation de la station sous forme de chaîne de caractères
        destinée à l'utilisateur.
        """
        return f"Station (ID: {self.dataset_id}, Créateur: {self.city})"

    def __repr__(self) -> str:
        """
        Retourne la représentation de l'objet Station.
        """
        return f"Station(dataset_id='{self.dataset_id}', creator='{self.city}')"