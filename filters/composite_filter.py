""" Implémentation du Design Pattern Composite pour enchaîner plusieurs filtres. """
import pandas as pd
from typing import List
from interfaces.base_interfaces import DataFilter

class CompositeFilter(DataFilter):
    """
    Un filtre qui applique séquentiellement une liste d'autres filtres.
    """

    def __init__(self, filters: List[DataFilter]):
        """
        Initialise le filtre composite.

        Args:
            filters (List[DataFilter]): Une liste de filtres qui seront appliquées dans l'ordre fourni.
        """
        
        self.filters = filters

    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applique chaque filtre de la liste au DataFrame, l'un après l'autre.

        Le DataFrame est passé à travers chaque filtre, le résultat d'un filtre
        devenant l'entrée du suivant.

        Args:
            df (DataFrame): Le DataFrame initial à filtrer.

        Returns:
            DataFrame: Le DataFrame final après l'application de tous les filtres.
        """

        processed_df = df.copy()
        
        for data_filter in self.filters:
            processed_df = data_filter.filter(processed_df)
            
        return processed_df