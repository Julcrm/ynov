""" Ce module définit des classes de base servant d'interfaces """

from typing import List
import pandas as pd

class DataLoader:
    """ Classe de base pour une classe chargée de charger des données. """
    def load_data(self) -> pd.DataFrame:

        raise NotImplementedError("Cette méthode doit être implémentée par la sous-classe")


class DataFilter:
    """ Classe de base pour une classe chargée de filtrer des données. """
    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applique un filtre sur un DataFrame.

        Args:
            - df (dataframe): Le DataFrame sur lequel appliquer le filtre.

        Returns: Le DataFrame une fois filtré.
        """
        raise NotImplementedError("Cette méthode doit être implémentée par la sous-classe")


class UserInterface:
    """ Classe de base pour une classe gérant l'interaction avec l'utilisateur. """
    def display_message(self, message: str) -> None:
        """
        Affiche un message à l'utilisateur.

        Args:
            - message (str): Le message qui sera affiché.
        """
        raise NotImplementedError("Cette méthode doit être implémentée par la sous-classe")

    def prompt_for_choice(self, choices: List[str], prompt: str) -> str:
        """
        Demande à l'utilisateur de faire un choix parmi une liste.

        Args:
           - choices (List[str]): La liste des options proposées à l'utilisateur.
           -  prompt (str): Le message affiché pour inviter l'utilisateur à choisir.

        Returns: Le choix qui a été sélectionné par l'utilisateur.
        """
        raise NotImplementedError("Cette méthode doit être implémentée par la sous-classe")