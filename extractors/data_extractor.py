""" Extracteur de données configuré pour un type de DataFrame spécifique. """
import pandas as pd
from typing import List, Any


class DataExtractor:
    """
    Extrait des informations spécifiques d'un DataFrame en se basant sur une
    configuration de colonnes fournie à l'initialisation.
    """

    def __init__(self, city_col: str, station_id_col: str, timestamp_col: str):
        """
        Initialise l'extracteur avec les noms des colonnes cibles.

        Args:
            city_col (str): Nom de la colonne contenant les noms des villes.
            station_id_col (str): Nom de la colonne contenant les ID des stations.
            timestamp_col (str): Nom de la colonne contenant les informations horaires.
        """
        self.city_col = city_col
        self.station_id_col = station_id_col
        self.timestamp_col = timestamp_col

    def get_unique_cities(self, df: pd.DataFrame) -> List[str]:
        """
        Extrait la liste triée des villes uniques à partir de la colonne configurée.
        """
        # On utilise l'attribut self.city_col configuré dans le __init__
        return self._extract_unique_sorted_values(df, self.city_col)

    def get_unique_stations(self, df: pd.DataFrame) -> List[str]:
        """
        Extrait la liste triée des stations uniques à partir de la colonne configurée.
        """
        # On utilise l'attribut self.station_id_col
        return self._extract_unique_sorted_values(df, self.station_id_col)

    def get_station_infos(self, df: pd.DataFrame) -> List[Any]:
        """
        Extrait les informations horaires à partir de la colonne configurée.
        """
        # On utilise l'attribut self.timestamp_col
        if df.empty or self.timestamp_col not in df.columns:
            return []
            
        return df[self.timestamp_col].dropna().tolist()

    def _extract_unique_sorted_values(self, df: pd.DataFrame, column_name: str) -> List[str]:
        """
        Méthode utilitaire pour extraire, nettoyer et trier les valeurs uniques.
        
        Args:
            df (DataFrame): Le DataFrame source.
            column_name (str): Le nom de la colonne à traiter.

        Returns:
            List[str]: Une liste triée de valeurs uniques.
            
        Raises:
            KeyError: Si la colonne n'existe pas dans le DataFrame.
        """
        if column_name not in df.columns:
            raise KeyError(f"La colonne '{column_name}' est introuvable.")
            
        return df[column_name].dropna().drop_duplicates().sort_values().tolist()