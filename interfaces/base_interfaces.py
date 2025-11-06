"""Interfaces de base pour le système"""


class DataLoader:
    """Classe de base pour le chargement de données"""
    def load_data(self):
        raise NotImplementedError("Cette méthode doit être implémentée")


class DataFilter:
    """Classe de base pour le filtrage de données"""
    def filter(self, df):
        raise NotImplementedError("Cette méthode doit être implémentée")


class UserInterface:
    """Classe de base pour l'interaction utilisateur"""
    def display_message(self, message):
        raise NotImplementedError("Cette méthode doit être implémentée")

    def prompt_for_choice(self, choices, prompt):
        raise NotImplementedError("Cette méthode doit être implémentée")