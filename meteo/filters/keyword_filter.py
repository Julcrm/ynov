"""Filtre pour inclure/exclure des lignes basées sur des mots-clés dans une colonne."""
import pandas as pd
from typing import Optional
from ..interfaces.base_interfaces import DataFilter


class KeywordFilter(DataFilter):
    """
    Filtre un DataFrame en se basant sur la présence ou l'absence de mots-clés
    dans une colonne textuelle.
    """

    def __init__(self, column_name: str, include_keyword: str, exclude_keyword: Optional[str] = None):
        """
        Initialise le filtre par mots-clés.

        Args:
            column_name (str): Le nom de la colonne sur laquelle filtrer.
            include_keyword (str): Le mot-clé que la colonne doit contenir.
            exclude_keyword (Optional[str], optional): Le mot-clé que la colonne
                                                       ne doit PAS contenir.
        """
        self.column_name = column_name
        self.include_keyword = include_keyword
        self.exclude_keyword = exclude_keyword

    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applique le filtre sur le DataFrame.
pip
        Args:
            df (DataFrame): Le DataFrame à filtrer.

        Returns:
            DataFrame: Un nouveau DataFrame contenant les lignes filtrées.
            
        Raises:
            KeyError: Si la colonne spécifiée n'existe pas dans le DataFrame.
        """
        if self.column_name not in df.columns:
            raise KeyError(f"La colonne '{self.column_name}' est introuvable.")

        # Condition de base : le mot-clé d'inclusion doit être présent
        include_condition = df[self.column_name].str.contains(
            self.include_keyword, case=False, na=False
        )

        # Si un mot-clé d'exclusion est fourni, on l'ajoute à la condition
        if self.exclude_keyword:
            exclude_condition = ~df[self.column_name].str.contains(
                self.exclude_keyword, case=False, na=False
            )
            final_condition = include_condition & exclude_condition
        else:
            final_condition = include_condition
        
        return df[final_condition].copy()