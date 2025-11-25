"""Loader pour les données de stations météo spécifiques."""
import requests
import pandas as pd
from typing import Dict, Any
from interfaces.base_interfaces import ParameterizedDataLoader


class StationDataLoader(ParameterizedDataLoader):
    """
    Charge les données pour une station météo spécifique en utilisant
    un modèle d'URL.
    """

    def __init__(self, api_url_template: str):
        """
        Initialise le loader avec un modèle d'URL.

        Args:
            api_url_template (str): 
                Un modèle d'URL formatable qui doit contenir {station_id}.
                Ex: "https://.../datasets/{station_id}/records"
        """
        self.api_url_template = api_url_template


    def load_data(self, station_id: str) -> pd.DataFrame:
        """
        Charge les données pour une station météo donnée.

        Args:
            station_id (str): ID de la station à charger.

        Returns:
            DataFrame: Un DataFrame contenant les enregistrements de la station.
        """
        url = self.api_url_template.format(station_id=station_id)
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()

            records: list[Dict[str, Any]] = data.get('results', [])

            if not records:

                return pd.DataFrame()

            return pd.DataFrame(records)


        except requests.exceptions.RequestException:
            # Retourne un DataFrame vide en cas d'erreur (station inexistante, 400, etc.)
            return pd.DataFrame()