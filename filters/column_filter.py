"""Filtre pour sélectionner un sous-ensemble de colonnes d'un DataFrame."""
import pandas as pd
from typing import List
from interfaces.base_interfaces import DataFilter


class ColumnFilter(DataFilter):
    """Filtre pour sélectionner une liste prédéfinie de colonnes dans un DataFrame."""

    def __init__(self, columns_to_keep: List[str]):
        """
        Initialise le filtre avec la liste des colonnes à conserver.

        Args:
            columns_to_keep (List[str]): La liste des noms de colonnes à garder.
        """
        self.columns_to_keep = columns_to_keep

    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filtre le DataFrame pour ne conserver que les colonnes spécifiées.

        Args:
            df (DataFrame): Le DataFrame à filtrer.

        Returns:
            DataFrame: Un nouveau DataFrame contenant uniquement les colonnes sélectionnées.
        """
        if df.empty:
            return df.copy()

        existing_columns = [col for col in self.columns_to_keep if col in df.columns]

        # Retourne une copie du DataFrame avec seulement les colonnes existantes
        return df[existing_columns].copy()