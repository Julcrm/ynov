"""Orchestrateur du workflow de sélection des stations météo"""


class WeatherStationOrchestrator:
    """
    Responsabilité unique: Orchestrer le workflow complet de sélection
    Cette classe coordonne les services mais ne fait pas le travail elle-même
    """

    def __init__(self, data_service, selection_service, ui):
        self.data_service = data_service
        self.selection_service = selection_service
        self.ui = ui

    def run_selection_workflow(self):
        """
        Exécute le workflow complet de sélection ville + station + chargement données
        Retourne (ville, station, données_station) ou None en cas d'échec
        """
        # Étape 1: Chargement du catalogue
        df_meteo = self._load_catalog_step()
        if df_meteo is None:
            return None

        # Étape 2: Sélection de la ville
        chosen_city = self._select_city_step(df_meteo)
        if not chosen_city:
            return None

        # Étape 3: Sélection de la station
        chosen_station = self._select_station_step(df_meteo, chosen_city)
        if not chosen_station:
            return None

        # Étape 4: Chargement des données de la station
        station_data = self._load_station_data_step(chosen_station)
        if station_data is None:
            return None

        # Étape 5: Filtrage des colonnes
        filtered_data = self._filter_station_data_step(station_data)
        if filtered_data is None:
            return None

        # Étape 6: Affichage des données filtrées
        self._display_station_data(filtered_data)

        return (chosen_city, chosen_station, filtered_data)

    def _load_catalog_step(self):
        """Étape 1: Charge le catalogue des stations météo"""
        self.ui.display_header("Chargement du catalogue")
        df_meteo = self.data_service.load_meteo_catalog()

        if df_meteo is None or df_meteo.empty:
            self.ui.display_message("Impossible de charger le catalogue.")
            return None

        self.ui.display_message(f"✓ {len(df_meteo)} stations trouvées")
        return df_meteo

    def _select_city_step(self, df_meteo):
        """Étape 2: Sélectionne une ville"""
        cities = self.data_service.get_cities(df_meteo)
        return self.selection_service.select_item_from_list(
            cities,
            "Choisissez une ville :",
            "Sélection de la ville"
        )

    def _select_station_step(self, df_meteo, city_name):
        """Étape 3: Sélectionne une station pour la ville choisie"""
        stations = self.data_service.get_stations_for_city(df_meteo, city_name)
        return self.selection_service.select_item_from_list(
            stations,
            f"Choisissez une station pour '{city_name}' :",
            "Sélection de la station"
        )

    def _load_station_data_step(self, station_id):
        """Étape 4: Charge les données de la station (déjà triées par l'API)"""
        station_data = self.data_service.load_station_data(station_id)

        if station_data is None:
            self.ui.display_message("Impossible de charger les données de la station.")
            return None

        return station_data

    def _filter_station_data_step(self, station_data):
        """Étape 5: Filtre les colonnes des données de la station"""
        filtered_data = self.data_service.filter_station_columns(station_data)

        if filtered_data is None:
            self.ui.display_message("Erreur lors du filtrage des colonnes.")
            return None

        self.ui.display_message(f"✓ Données filtrées ({len(filtered_data.columns)} colonnes conservées)")
        return filtered_data

    def _display_station_data(self, station_data):
        """Étape 6: Affiche les données filtrées de la station"""
        self.ui.display_header("Données de la station (triées par date décroissante)")
        self.ui.display_dataframe(station_data, max_rows=10)

    def get_infos_for_station(self, station_data):
        """Récupère les informations depuis les données filtrées de la station"""
        return self.data_service.get_station_infos(station_data)