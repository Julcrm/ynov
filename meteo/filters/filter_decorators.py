import pandas as pd
from ..interfaces.base_interfaces import DataFilter

class FilterDecorator(DataFilter):
    """
    Classe de base pour les décorateurs de filtres.
    Maintient une référence vers un objet DataFilter et délègue le travail.
    C'est le composant central du pattern Decorator.
    """
    def __init__(self, wrapped_filter: DataFilter):
        self._wrapped_filter = wrapped_filter

    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Délègue l'appel au composant décoré."""
        return self._wrapped_filter.filter(df)


class LoggingDecorator(FilterDecorator):
    """
    Exemple concret de décorateur : ajoute du logging.
    Enveloppe n'importe quel DataFilter pour afficher des infos avant/après.
    """
    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        print(f"[LOG] Application du filtre : {type(self._wrapped_filter).__name__}")
        print(f"[LOG] Lignes avant : {len(df)}")
        
        # Appel au parent qui appelle le filtre enveloppé
        result = super().filter(df)
        
        print(f"[LOG] Lignes après : {len(result)}")
        return result
