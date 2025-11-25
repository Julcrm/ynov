""" Service de façade pour simplifier l'accès et le traitement des données météo."""
import pandas as pd
from typing import List, Optional
from interfaces.base_interfaces import DataLoader, DataFilter, ParameterizedDataLoader
from extractors.data_extractor import DataExtractor
from models.station import Station
from interfaces.navigation_interface import StationNavigator
from factories.station_navigator_factory import StationNavigatorFactory


class WeatherDataService:
    """
    Ce service coordonne les loaders, filtres et extracteurs.
    Il est configuré via l'injection de dépendances.
    """

    def __init__(
        self,
        catalog_loader: DataLoader,
        station_loader: ParameterizedDataLoader,
        catalog_filter: DataFilter,
        city_filter_factory,
        column_filter: DataFilter,
        extractor: DataExtractor,
        navigator_factory: StationNavigatorFactory
    ):
        """
        Initialise le service avec toutes les dépendances nécessaires.

        Args:
            catalog_loader: Loader pour le catalogue de stations.
            station_loader: Loader pour les données d'une station spécifique.
            catalog_filter: Filtre à appliquer sur le catalogue brut.
            city_filter_factory: Une fonction ou classe capable de créer un filtre de ville
            column_filter: Filtre pour sélectionner les colonnes utiles des données de station.
            extractor: Extracteur de données configuré.
        """
        self.catalog_loader = catalog_loader
        self.station_loader = station_loader
        self.navigator_factory = navigator_factory
        self.catalog_filter = catalog_filter
        self.city_filter_factory = city_filter_factory
        self.column_filter = column_filter
        self.extractor = extractor
        self.processed_catalog: Optional[pd.DataFrame] = None

    def get_processed_catalog(self) -> pd.DataFrame:
        """
        Charge et filtre le catalogue des stations météo.
        Met en cache le résultat pour éviter de le recharger.
        """
        # Mise en cache simple pour ne pas recharger à chaque fois
        if self.processed_catalog is None:
            raw_catalog = self.catalog_loader.load_data()
            if raw_catalog.empty:
                self.processed_catalog = pd.DataFrame()
            else:
                self.processed_catalog = self.catalog_filter.filter(raw_catalog)

        return self.processed_catalog

    def get_cities(self) -> List[str]:
        """Récupère la liste des villes depuis le catalogue filtré."""
        catalog = self.get_processed_catalog()
        return self.extractor.get_unique_cities(catalog)

    def get_stations_for_city(self, city_name: str) -> StationNavigator:
        """Récupère un navigateur de stations pour une ville donnée."""
        catalog = self.get_processed_catalog()
        city_filter = self.city_filter_factory(city_name)

        city_specific_catalog = city_filter.filter(catalog)
        station_ids = self.extractor.get_unique_stations(city_specific_catalog)

        # Créer des objets Station à partir des IDs
        stations = [Station(station_id, city_name) for station_id in station_ids]

        # Utiliser la factory pour créer le navigateur
        return self.navigator_factory.create_from_station_list(stations)

    def get_station_data(self, station_id: str) -> pd.DataFrame:
        """
        Charge et filtre les données pour une station unique.
        Retourne un DataFrame avec uniquement les colonnes utiles.
        """
        raw_station_data = self.station_loader.load_data(station_id)
        if raw_station_data.empty:
            return pd.DataFrame()

        return self.column_filter.filter(raw_station_data)