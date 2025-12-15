"""
Point d'entrée de l'application.
Responsable de la configuration et de l'assemblage des composants.
"""

# --- Imports des classes concrètes ---
from .loaders.station_data_loader import StationDataLoader
from .extractors.data_extractor import DataExtractor
from .filters.city_filter import CityFilter
from .filters.keyword_filter import KeywordFilter
from .filters.column_filter import ColumnFilter
from .filters.composite_filter import CompositeFilter
from .ui.interactive_ui import InteractiveConsoleUI
from .services.weather_data_service import WeatherDataService
from .services.user_selection_service import UserSelectionService
from .orchestrator.weather_station_orchestrator import WeatherStationOrchestrator
from .factories.station_navigator_factory import StationNavigatorFactory
from .loaders.cities_loader import CitiesLoader
from .config_loader import load_config


def main():
    """Charge la config, configure les composants et exécute l'application."""

    # =========================================================================
    # 1. CHARGEMENT DE LA CONFIGURATION EXTERNE
    # =========================================================================
    config = load_config()

    # =========================================================================
    # 2. CRÉATION ET ASSEMBLAGE DES COMPOSANTS
    # =========================================================================

    # --- Couche d'accès aux données (Loaders) ---
    cities_loader = CitiesLoader(catalog_url=config['api']['cities_url'])
    station_loader = StationDataLoader(api_url_template=config['api']['station_template_url'])

    # --- Couche de présentation (UI) ---
    ui = InteractiveConsoleUI()

    # --- Couche de traitement (Filtres & Extracteur) ---
    extractor = DataExtractor(
        city_col=config['columns']['city'],
        station_id_col=config['columns']['station_id'],
        timestamp_col=config['columns']['timestamp']
    )

    meteo_keyword_filter = KeywordFilter(
        column_name=config['columns']['station_id'],
        include_keyword=config['filters']['meteo_keyword'],
        exclude_keyword=config['filters']['archive_keyword']
    )

    city_filter_factory = lambda city: CityFilter(column_name=config['columns']['city'], city_name=city)

    station_data_column_filter = ColumnFilter(columns_to_keep=config['columns']['meteo_to_keep'])

    navigator_factory = StationNavigatorFactory()

    catalog_processing_pipeline = CompositeFilter([meteo_keyword_filter])

    # --- Couche de Services (Coordination) ---
    data_service = WeatherDataService(
        catalog_loader=cities_loader,
        station_loader=station_loader,
        catalog_filter=catalog_processing_pipeline,
        city_filter_factory=city_filter_factory,
        column_filter=station_data_column_filter,
        extractor=extractor,
        navigator_factory = navigator_factory
    )

    selection_service = UserSelectionService(ui=ui)

    # --- Orchestrateur ---
    orchestrator = WeatherStationOrchestrator(
        data_service=data_service,
        selection_service=selection_service,
        ui=ui
    )

    # =========================================================================
    # 3. LANCEMENT DE L'APPLICATION
    # =========================================================================
    orchestrator.run()


if __name__ == "__main__":
    main()