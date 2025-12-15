"""Orchestrateur du workflow de l'application."""
import requests
import re
from ..services.weather_data_service import WeatherDataService
from ..services.user_selection_service import UserSelectionService
from ..interfaces.base_interfaces import UserInterface
from ..commands.navigation_commands import NextStationCommand, PreviousStationCommand
from ..commands.workflow_commands import QuitCommand, RestartWorkflowCommand



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

        # Étape 3: Récupérer le navigateur de stations
        station_navigator = self.data_service.get_stations_for_city(chosen_city)
        if station_navigator.get_total() == 0:
            self.ui.display_message("Aucune station trouvée pour cette ville.")
            return

        # Fonction pour nettoyer l'affichage des noms de stations
        def clean_station_name(station_id: str) -> str:
            """Formate un ID de station pour un affichage plus lisible."""
            if "stations-meteo-en-place" in station_id:
                return "Catalogue général des stations (info)"
            name_without_prefix = re.sub(r'^\d+-', '', station_id)
            cleaned_name = name_without_prefix.replace('-', ' ').capitalize()
            return cleaned_name

        # Construire la liste des stations pour le choix initial
        stations_list = []
        temp_navigator = station_navigator
        for i in range(station_navigator.get_total()):
            current = temp_navigator.get_current()
            if current:
                display_name = clean_station_name(current.dataset_id)
                stations_list.append(display_name)
            if temp_navigator.has_next():
                temp_navigator.next()

        # Réinitialiser le navigateur
        station_navigator.reset()

        # Sélection initiale de la station
        chosen_display_name = self.selection_service.select_item_from_list(
            stations_list,
            prompt=f"Veuillez choisir une station pour '{chosen_city}' :",
            header="SÉLECTION DE LA STATION"
        )

        if not chosen_display_name:
            self.ui.display_message("Aucune station sélectionnée. Fin du programme.")
            return

        # Positionner le navigateur sur la station choisie
        chosen_index = stations_list.index(chosen_display_name)
        station_navigator.reset()
        for _ in range(chosen_index):
            station_navigator.next()

        # Boucle d'affichage des données avec navigation
        while True:
            current_station = station_navigator.get_current()
            if current_station is None:
                self.ui.display_message("Erreur : aucune station courante.")
                return

            # Étape 4: Charger et afficher les données de la station courante
            position = station_navigator.get_position()
            total = station_navigator.get_total()
            display_name = clean_station_name(current_station.dataset_id)

            self.ui.display_header(f"STATION ({position}/{total}) : {display_name}")
            self.ui.display_message(f"ID: {current_station.dataset_id}")
            self.ui.display_message("Chargement des données...")

            station_data = self.data_service.get_station_data(current_station.dataset_id)

            if station_data.empty:
                self.ui.display_message("⚠ Aucune donnée disponible pour cette station.")
            else:
                self.ui.display_message("✓ Données chargées et colonnes filtrées.")
                self.ui.display_header("APERÇU DES DERNIÈRES DONNÉES")
                self.ui.display_dataframe(station_data)

            # Options de navigation après affichage
            # Création des commandes (Pattern Command)
            navigation_options = {}
            if station_navigator.has_previous():
                navigation_options["← Station précédente"] = PreviousStationCommand(station_navigator)
            
            if station_navigator.has_next():
                navigation_options["Station suivante →"] = NextStationCommand(station_navigator)
                
            navigation_options["⟲ Choisir une autre station"] = RestartWorkflowCommand()
            navigation_options["✗ Quitter"] = QuitCommand(self.ui)

            choices = list(navigation_options.keys())
            
            user_choice = self.ui.prompt_for_choice(
                choices=choices,
                prompt="Que voulez-vous faire ?"
            )

            if user_choice not in navigation_options:
                # Cas par défaut ou None (Quitter)
                QuitCommand(self.ui).execute()
                return

            command = navigation_options[user_choice]
            should_continue = command.execute()

            # Gestion spécifique pour le redémarrage (car Command.execute retourne juste un bool pour continuer ou pas la boucle locale)
            if isinstance(command, RestartWorkflowCommand):
                self._execute_workflow() # Récursion pour redémarrer
                return
            
            if not should_continue:
                return