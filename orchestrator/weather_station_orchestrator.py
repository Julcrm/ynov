"""Orchestrateur du workflow de l'application."""
import requests
import re
from services.weather_data_service import WeatherDataService
from services.user_selection_service import UserSelectionService
from interfaces.base_interfaces import UserInterface



class WeatherStationOrchestrator:
    """
    Orchestre l'application en coordonnant les services.
    """

    def __init__(
        self,
        data_service: WeatherDataService,
        selection_service: UserSelectionService,
        ui: UserInterface
    ):
        self.data_service = data_service
        self.selection_service = selection_service
        self.ui = ui

    def run(self):
        """
        Exécute le workflow principal de l'application.
        Gère les erreurs et les affiche à l'utilisateur.
        """
        try:
            # Le workflow est encapsulé pour attraper les erreurs
            self._execute_workflow()
        except requests.exceptions.RequestException as e:
            self.ui.display_header("ERREUR CRITIQUE DE CONNEXION")
            self.ui.display_message(f"Impossible de récupérer les données : {e}")
            self.ui.display_message("Veuillez vérifier votre connexion internet ou l'URL de l'API.")
        except KeyError as e:
            self.ui.display_header("ERREUR DE CONFIGURATION")
            self.ui.display_message(f"Une colonne attendue n'a pas été trouvée : {e}")
            self.ui.display_message("Vérifiez les noms de colonnes dans la configuration.")
        except Exception as e:
            self.ui.display_header("ERREUR INCONNUE")
            self.ui.display_message(f"Une erreur inattendue est survenue : {e}")

    def _execute_workflow(self):
        """Définit la séquence des opérations du workflow."""
        # Étape 1: Obtenir le catalogue de stations

        self.ui.display_header("APPLICATION MÉTÉO")
        self.ui.display_message("Initialisation : chargement du catalogue des stations...")

        catalog = self.data_service.get_processed_catalog()
        if catalog.empty:
            self.ui.display_message("Le catalogue de stations est vide ou n'a pas pu être chargé.")
            return

        self.ui.display_message(f"✓ {len(catalog)} stations météo trouvées dans le catalogue.")

        # Étape 2: Sélectionner une ville
        cities = self.data_service.get_cities()
        chosen_city = self.selection_service.select_item_from_list(
            cities,
            prompt="Veuillez choisir une ville :",
            header="SÉLECTION DE LA VILLE"
        )
        if not chosen_city:
            self.ui.display_message("Aucune ville sélectionnée. Fin du programme.")
            return

        # Étape 3: Sélectionner une station
        stations_ids = self.data_service.get_stations_for_city(chosen_city)
        if not stations_ids:
            self.ui.display_message("Aucune station trouvée pour cette ville.")
            return

        # --- AMÉLIORATION DE L'AFFICHAGE ---

        def clean_station_name(station_id: str) -> str:
            """Formate un ID de station pour un affichage plus lisible."""
            # Cas spécial pour la dernière ligne
            if "stations-meteo-en-place" in station_id:
                return "Catalogue général des stations (info)"

            # Retire le préfixe numérique (ex: "42-")
            name_without_prefix = re.sub(r'^\d+-', '', station_id)
            # Remplace les tirets par des espaces et met en majuscule la première lettre
            cleaned_name = name_without_prefix.replace('-', ' ').capitalize()
            return cleaned_name

        # On crée la liste des noms à afficher à l'utilisateur
        station_display_names = [clean_station_name(s_id) for s_id in stations_ids]

        # On demande à l'utilisateur de choisir parmi les noms propres
        chosen_display_name = self.selection_service.select_item_from_list(
            station_display_names,
            prompt=f"Veuillez choisir une station pour '{chosen_city}' :",
            header="SÉLECTION DE LA STATION"
        )

        if not chosen_display_name:
            self.ui.display_message("Aucune station sélectionnée. Fin du programme.")
            return

        # On retrouve l'ID original qui correspond au nom choisi par l'utilisateur
        chosen_index = station_display_names.index(chosen_display_name)
        chosen_station = stations_ids[chosen_index]

        # Étape 4: Obtenir les données de la station (chargement + filtrage)
        self.ui.display_header(f"CHARGEMENT DES DONNÉES POUR '{chosen_station}'")
        station_data = self.data_service.get_station_data(chosen_station)
        if station_data.empty:
            self.ui.display_message("Aucune donnée disponible pour cette station.")
            return

        self.ui.display_message("✓ Données chargées et colonnes filtrées.")

        # Étape 5: Afficher les données
        self.ui.display_header("APERÇU DES DERNIÈRES DONNÉES")
        self.ui.display_dataframe(station_data)