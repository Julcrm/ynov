"""Loader pour le catalogue des villes depuis une URL."""
import requests
import pandas as pd
from io import StringIO
from ..interfaces.base_interfaces import DataLoader




class CitiesLoader(DataLoader):
    """
    Charge le catalogue des villes depuis une URL fournissant un fichier CSV.
    """

    def __init__(self, catalog_url: str):
        """
        Initialise le loader avec l'URL du catalogue.

        Args:
            catalog_url (str): L'URL directe vers le fichier CSV des villes.
        """
        self.catalog_url = catalog_url

    def load_data(self) -> pd.DataFrame:
        """
        Charge les données depuis l'URL, les parse en CSV et les retourne en DataFrame.

        Returns:
            DataFrame: Un DataFrame contenant les données des villes.

        """
        try:
            # Réponse de la request
            response = requests.get(self.catalog_url)
            
            # Vérifie si la requête a réussi
            response.raise_for_status()

            # Lecture du CSV depuis le texte de la réponse
            df = pd.read_csv(StringIO(response.text), sep=";")
            return df

        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion à l'API : {e}")