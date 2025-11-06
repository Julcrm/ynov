"""Filtre pour sélectionner des données basées sur une colonne de type texte."""
import pandas as pd
from interfaces.base_interfaces import DataFilter


class CityFilter(DataFilter):
    """
    Filtre un DataFrame pour ne garder qu'une colonne spécifique
    """

    def __init__(self, column_name: str, city_name: str):
        """
        Initialise le filtre.

        Args:
            column_name (str): Le nom de la colonne sur laquelle appliquer le filtre.
            city_name (str): La valeur textuelle à rechercher dans la colonne.
        """
        self.column_name = column_name
        self.city_name = city_name

    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applique le filtre sur le DataFrame.

        Args:
            df (DataFrame): Le DataFrame à filtrer.

        Returns:
            DataFrame: Un nouveau DataFrame contenant uniquement la colonne voulus.

        Raises:
            KeyError: Si la colonne spécifiée n'existe pas dans le DataFrame.
        """
        # Vérifie que la colonne existe pour éviter une KeyError non gérée
        if self.column_name not in df.columns:
            raise KeyError(
                f"La colonne '{self.column_name}' n'a pas été trouvée "
                "dans le DataFrame."
            )

        # Condition de filtrage
        condition = df[self.column_name].str.contains(
            self.city_name, case=False, na=False
        )

        filtered_df = df[condition].copy()

        return filtered_df