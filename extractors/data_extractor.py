"""Extracteur de données spécifiques"""


class DataExtractor:
    """Responsabilité unique: Extraire des informations spécifiques du DataFrame"""

    def get_unique_cities(self, df):
        """Extrait la liste des villes uniques"""
        cities = df["dcat.creator"].drop_duplicates().dropna().sort_values().tolist()
        return cities

    def get_unique_stations(self, df):
        """Extrait la liste des stations uniques"""
        stations = df["datasetid"].drop_duplicates().dropna().sort_values().tolist()
        return stations

    def get_station_infos(self, df):
        """Extrait la liste des informations horaires de la station"""
        if df.empty or "heure_de_paris" not in df.columns:
            return []

        df_clean = df.dropna(subset=["heure_de_paris"])
        stations_infos = df_clean["heure_de_paris"].tolist()

        return stations_infos