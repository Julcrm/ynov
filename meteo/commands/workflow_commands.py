from ..interfaces.command_interface import Command
from ..interfaces.base_interfaces import UserInterface

class QuitCommand(Command):
    """Commande pour quitter l'application."""
    
    def __init__(self, ui: UserInterface):
        self.ui = ui
        
    def execute(self) -> bool:
        self.ui.display_message("Au revoir !")
        return False  # Indique qu'on doit arrêter la boucle

class RestartWorkflowCommand(Command):
    """Commande pour recommencer le workflow (choisir une autre ville/station)."""
    
    def __init__(self):
        pass
        
    def execute(self) -> bool:
        # Signale à l'orchestrateur de redémarrer (gestion spécifique nécessaire dans l'appelant)
        return False 
