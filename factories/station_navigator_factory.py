"""Factory pour créer des navigateurs de stations."""
from typing import List
import re
from models.station import Station
from interfaces.navigation_interface import StationNavigator
from services.station_linked_list import StationLinkedList


class StationNavigatorFactory:
  """
  Factory pour créer des instances de StationNavigator.
  Les stations sont automatiquement triées par ordre alphabétique d'ID.
  """

  def create_from_station_list(self, stations: List[Station]) -> StationNavigator:
      """
      Crée un navigateur de stations à partir d'une liste de stations.
      Les stations sont triées par nom (sans le préfixe numérique).

      Args:
          stations (List[Station]): La liste des stations à organiser.

      Returns:
          StationNavigator: Un navigateur de stations configuré et trié.
      """
      def get_name_without_prefix(station_id: str) -> str:
          """Extrait le nom sans le préfixe numérique (ex: '42-meteo-blagnac' -> 'meteo-blagnac')"""
          # Retire le préfixe numérique au début (ex: "42-")
          return re.sub(r'^\d+-', '', station_id).lower()

      # Trier les stations par nom (sans préfixe numérique), ordre alphabétique
      sorted_stations = sorted(stations, key=lambda s: get_name_without_prefix(s.dataset_id))

      # Créer la liste chaînée
      linked_list = StationLinkedList()

      # Ajouter toutes les stations à la liste
      for station in sorted_stations:
          linked_list.add_station(station)

      return linked_list