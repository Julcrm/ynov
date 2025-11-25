"""Implémentation d'une liste doublement chaînée pour les stations météo."""
from typing import Optional
from models.station import Station
from models.station_node import StationNode
from interfaces.navigation_interface import StationNavigator


class StationLinkedList(StationNavigator):
    """
    Liste doublement chaînée pour naviguer entre les stations.
    Implémente l'interface StationNavigator.
    """

    def __init__(self):
        """Initialise une liste chaînée vide."""
        self._head: Optional[StationNode] = None
        self._tail: Optional[StationNode] = None
        self._current: Optional[StationNode] = None
        self._size: int = 0

    def add_station(self, station: Station) -> None:
        """
        Ajoute une station à la fin de la liste.

        Args:
            station (Station): La station à ajouter.
        """
        new_node = StationNode(station)

        if self._head is None:
            # Liste vide : le nouveau nœud devient head et tail
            self._head = new_node
            self._tail = new_node
            self._current = new_node
        else:
            # Ajouter à la fin
            self._tail.next = new_node
            new_node.prev = self._tail
            self._tail = new_node

        self._size += 1

    def next(self) -> Optional[Station]:
        """
        Avance à la station suivante.

        Returns:
            Station: La station suivante, ou None si on est à la fin.
        """
        if self._current is None or self._current.next is None:
            return None

        self._current = self._current.next
        return self._current.station

    def previous(self) -> Optional[Station]:
        """
        Recule à la station précédente.

        Returns:
            Station: La station précédente, ou None si on est au début.
        """
        if self._current is None or self._current.prev is None:
            return None

        self._current = self._current.prev
        return self._current.station

    def get_current(self) -> Optional[Station]:
        """
        Retourne la station actuellement sélectionnée.

        Returns:
            Station: La station courante, ou None si la liste est vide.
        """
        if self._current is None:
            return None
        return self._current.station

    def has_next(self) -> bool:
        """
        Vérifie s'il existe une station suivante.

        Returns:
            bool: True si une station suivante existe, False sinon.
        """
        return self._current is not None and self._current.next is not None

    def has_previous(self) -> bool:
        """
        Vérifie s'il existe une station précédente.

        Returns:
            bool: True si une station précédente existe, False sinon.
        """
        return self._current is not None and self._current.prev is not None

    def reset(self) -> None:
        """Réinitialise la navigation au début (première station)."""
        self._current = self._head

    def get_position(self) -> int:
        """
        Retourne la position actuelle (1-indexed).

        Returns:
            int: La position de la station courante (commence à 1).
        """
        if self._current is None:
            return 0

        position = 1
        node = self._head
        while node is not None and node != self._current:
            position += 1
            node = node.next

        return position

    def get_total(self) -> int:
        """
        Retourne le nombre total de stations.

        Returns:
            int: Le nombre total de stations dans la liste.
        """
        return self._size

    def __str__(self) -> str:
        """Retourne une représentation lisible de la liste."""
        if self._size == 0:
            return "StationLinkedList(vide)"
        return f"StationLinkedList({self._size} stations, position={self.get_position()})"

    def __repr__(self) -> str:
        """Retourne la représentation de l'objet."""
        return f"StationLinkedList(size={self._size}, current_pos={self.get_position()})"