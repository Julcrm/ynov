"""Classe représentant un nœud dans la liste chaînée de stations."""
from typing import Optional
from .station import Station


class StationNode:
    """
    Représente un nœud dans une liste doublement chaînée de stations.
    Encapsule une station et maintient des références vers les nœuds adjacent.
    """

    def __init__(self, station: Station):
        """
        Initialise un nœud avec une station.

        Args :
            station (Station): La station à encapsuler dans ce nœud.
        """
        self.station = station
        self.next: Optional['StationNode'] = None
        self.prev: Optional['StationNode'] = None

    def __str__(self) -> str:
        """
        Retourne une représentation lisible du nœud.
        """
        return f"StationNode({self.station})"

    def __repr__(self) -> str:
        """
        Retourne la représentation de l'objet StationNode.
        """
        has_next = self.next is not None
        has_prev = self.prev is not None
        return f"StationNode(station={self.station}, has_next={has_next}, has_prev={has_prev})"
