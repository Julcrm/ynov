"""Loader pour les données d'une station spécifique"""
import requests
import pandas as pd
from interfaces.base_interfaces import DataLoader


class StationDataLoader(DataLoader):
    """Responsabilité unique: Charger les données d'une station spécifique"""

    def __init__(self, station_id):
        self.station_id = station_id

    def load_data(self):
        """Charge les données de la station depuis l'API (triées par date décroissante)"""
        url = f"https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/{self.station_id}/records?order_by=-heure_de_paris"

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            if 'results' in data:
                records = data['results']
                if not records:
                    print(f"Aucun enregistrement trouvé pour la station '{self.station_id}'")
                    return pd.DataFrame()

                df = pd.DataFrame(records)
                return df

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors du chargement des données de la station '{self.station_id}': {e}")
            return pd.DataFrame()