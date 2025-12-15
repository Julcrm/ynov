class Command:
    """Interface de base pour toutes les commandes."""

    def execute(self) -> bool:
        """
        Exécute la commande.
        
        Returns:
            bool: True si le workflow doit continuer, False s'il doit s'arrêter ou changer d'état significativement.
        """
        raise NotImplementedError("La méthode execute doit être implémentée par les sous-classes.")

