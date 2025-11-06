"""Loader pour le catalogue des villes"""
import requests
import pandas as pd
from io import StringIO
from interfaces.base_interfaces import DataLoader


class CitiesLoader(DataLoader):
    """Responsabilité unique: Charger les données depuis l'API"""

    def __init__(self):
        self.catalog_url = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/exports/csv?delimiter=%3B&list_separator=%2C&quote_all=false&with_bom=true"

    def load_data(self):
        try:
            response = requests.get(self.catalog_url)
            response.raise_for_status()
            df = pd.read_csv(StringIO(response.text), sep=";")
            return df
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion à l'API : {e}")
            return pd.DataFrame()