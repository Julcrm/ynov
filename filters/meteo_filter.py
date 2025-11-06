"""Filtre pour les données météo"""
from interfaces.base_interfaces import DataFilter


class MeteoFilter(DataFilter):
    """Filtre pour les données météo (exclut les archives)"""

    def filter(self, df):
        filtered_df = df[
            df["datasetid"].str.contains("meteo", case=False, na=False) &
            ~df["datasetid"].str.contains("archive", case=False, na=False)
        ].copy()
        return filtered_df