""" Implémentation du Design Pattern Composite pour enchaîner plusieurs filtres. """
import pandas as pd
from typing import List, Optional
from ..interfaces.base_interfaces import DataFilter
from .queue_structure import Queue


class CompositeFilter(DataFilter):
    """
    Un filtre qui applique séquentiellement des filtres stockés dans une file (Queue).
    Respecte le principe FIFO (First In, First Out).
    """

    def __init__(self, filters: Optional[List[DataFilter]] = None):
        """
        Initialise le filtre composite avec une file.

        Args:
            filters (Optional[List[DataFilter]]): Liste optionnelle de filtres initiaux.
        """

        self._filter_queue = Queue()

        if filters is not None:
            for data_filter in filters:
                self.add_filter(data_filter)

    def add_filter(self, data_filter: DataFilter) -> None:
        """
        Ajoute un filtre à la fin de la file.

        Args:
            data_filter (DataFilter): Le filtre à ajouter.

        Raises:
            TypeError: Si l'objet n'implémente pas DataFilter.
        """
        if not isinstance(data_filter, DataFilter):
            raise TypeError("Le filtre doit implémenter l'interface DataFilter")

        self._filter_queue.enqueue(data_filter)

    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applique chaque filtre de la file au DataFrame, l'un après l'autre.

        La file n'est pas vidée définitivement: les filtres sont temporairement
        extraits puis remis dans la file pour permettre une réutilisation.

        Args:
            df (DataFrame): Le DataFrame initial à filtrer.

        Returns:
            DataFrame: Le DataFrame final après l'application de tous les filtres.
        """
        processed_df = df.copy()

        temp_filters = []

        while not self._filter_queue.is_empty():
            current_filter = self._filter_queue.dequeue()

            processed_df = current_filter.filter(processed_df)

            temp_filters.append(current_filter)

        # Remettre tous les filtres dans la queue pour préserver l'état
        # (permet de réutiliser le CompositeFilter plusieurs fois)
        for filter_item in temp_filters:
            self._filter_queue.enqueue(filter_item)

        return processed_df

    def is_empty(self) -> bool:
        """
        Vérifie si la file de filtres est vide.

        Returns:
            bool: True si la file est vide, False sinon.
        """
        return self._filter_queue.is_empty()

    def size(self) -> int:
        """
        Retourne le nombre de filtres dans la file.

        Returns:
            int: Le nombre de filtres.
        """
        return self._filter_queue.size()

    def clear_filters(self) -> None:
        """
        Vide tous les filtres de la file.
        """
        self._filter_queue.clear()

    def __str__(self) -> str:
        """
        Représentation textuelle du filtre composite.

        Returns:
            str: Description du composite.
        """
        return f"CompositeFilter(nombre de filtres: {self.size()})"