"""Service de gestion des données météo"""
from filters.meteo_filter import MeteoFilter
from filters.city_filter import CityFilter
from filters.column_filter import ColumnFilter
from filters.composite_filter import CompositeFilter
from loaders.station_data_loader import StationDataLoader


class WeatherDataService:
    """
    Responsabilité unique: Gérer le chargement et le filtrage des données météo
    """

    def __init__(self, catalog_loader, extractor, column_filter=None):
        self.catalog_loader = catalog_loader
        self.extractor = extractor
        self.column_filter = column_filter or ColumnFilter()

    def load_meteo_catalog(self):
        """Charge et filtre le catalogue des stations météo"""
        df = self.catalog_loader.load_data()
        if df.empty:
            return None

        meteo_filter = MeteoFilter()
        return meteo_filter.filter(df)

    def get_cities(self, df):
        """Récupère la liste des villes depuis le DataFrame"""
        return self.extractor.get_unique_cities(df)

    def get_stations_for_city(self, df, city_name):
        """Récupère les stations pour une ville donnée"""
        meteo_filter = MeteoFilter()
        city_filter = CityFilter(city_name)
        combined_filter = CompositeFilter([meteo_filter, city_filter])
        df_filtered = combined_filter.filter(df)
        return self.extractor.get_unique_stations(df_filtered)

    def load_station_data(self, station_id):
        """
        Charge les données d'une station (déjà triées par l'API)
        Retourne un DataFrame ou None si vide
        """
        station_loader = StationDataLoader(station_id)
        df_station = station_loader.load_data()

        if df_station.empty:
            return None

        return df_station

    def filter_station_columns(self, df):
        """
        Applique le filtre de colonnes
        Retourne un DataFrame filtré
        """
        if df is None or df.empty:
            return None

        return self.column_filter.filter(df)

    def get_station_infos(self, df):
        """Récupère les informations depuis le DataFrame filtré"""
        return self.extractor.get_station_infos(df)