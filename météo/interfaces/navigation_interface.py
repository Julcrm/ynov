"""Interface pour la navigation entre les stations météo."""

class StationNavigator:
    """
    Classe de base pour naviguer entre les stations météo.
    Permet une navigation bidirectionnelle dans une collection de stations.
    """

    def next(self):
        """
        Avance à la station suivante.

        Returns :
            Station : La station suivante, ou None si on est à la fin.
        """
        raise NotImplementedError("Cette méthode doit être implémentée par la sous-classe")

    def previous(self):
        """
        Recule à la station précédente.

        Returns :
            Station : La station précédente, ou None si on est au début.
        """
        raise NotImplementedError("Cette méthode doit être implémentée par la sous-classe")

    def get_current(self):
        """
        Retourne la station actuellement sélectionnée.

        Returns:
            Station: La station courante, ou None si la liste est vide.
        """
        raise NotImplementedError("Cette méthode doit être implémentée par la sous-classe")

    def has_next(self) -> bool:
        """
        Vérifie s'il existe une station suivante.

        Returns:
            bool: True si une station suivante existe, False sinon.
        """
        raise NotImplementedError("Cette méthode doit être implémentée par la sous-classe")

    def has_previous(self) -> bool:
        """
        Vérifie s'il existe une station précédente.

        Returns :
            bool : True si une station précédente existe, False sinon.
        """
        raise NotImplementedError("Cette méthode doit être implémentée par la sous-classe")

    def reset(self) -> None:
        """
        Réinitialise la navigation au début (première station).
        """
        raise NotImplementedError("Cette méthode doit être implémentée par la sous-classe")

    def get_position(self) -> int:
        """
        Retourne la position actuelle (1-indexed).

        Returns :
            int : La position de la station courante (commence à 1).
        """
        raise NotImplementedError("Cette méthode doit être implémentée par la sous-classe")

    def get_total(self) -> int:
        """
        Retourne le nombre total de stations.

        Returns :
            int : Le nombre total de stations dans la liste.
        """
        raise NotImplementedError("Cette méthode doit être implémentée par la sous-classe")
