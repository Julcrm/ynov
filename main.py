"""Point d'entrée de l'application"""
from loaders.cities_loader import CitiesLoader
from extractors.data_extractor import DataExtractor
from filters.column_filter import ColumnFilter
from ui.console_ui import ConsoleUserInterface
from services.weather_data_service import WeatherDataService
from services.user_selection_service import UserSelectionService
from orchestrator.weather_station_orchestrator import WeatherStationOrchestrator


def main():
    """
    Configuration et injection de dépendances
    Respect du principe D (Dependency Inversion)
    """
    # Création des composants de base
    catalog_loader = CitiesLoader()
    ui = ConsoleUserInterface()
    extractor = DataExtractor()

    # Création des filtres
    column_filter = ColumnFilter()

    # Création des services spécialisés (injection de dépendances)
    data_service = WeatherDataService(
        catalog_loader,
        extractor,
        column_filter
    )
    selection_service = UserSelectionService(ui)

    # Création de l'orchestrateur (injection de dépendances)
    orchestrator = WeatherStationOrchestrator(data_service, selection_service, ui)

    orchestrator.run_selection_workflow()


if __name__ == "__main__":
    main()