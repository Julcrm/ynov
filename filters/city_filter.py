"""Filtre pour une ville spécifique"""
from interfaces.base_interfaces import DataFilter


class CityFilter(DataFilter):
    """Filtre pour une ville spécifique"""

    def __init__(self, city_name):
        self.city_name = city_name

    def filter(self, df):
        filtered_df = df[
            df["dcat.creator"].str.contains(self.city_name, case=False, na=False)
        ].copy()
        return filtered_df