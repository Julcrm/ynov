from ..interfaces.command_interface import Command
from ..interfaces.navigation_interface import StationNavigator

class NextStationCommand(Command):
    """Commande pour passer à la station suivante."""
    
    def __init__(self, navigator: StationNavigator):
        self.navigator = navigator
        
    def execute(self) -> bool:
        self.navigator.next()
        return True

class PreviousStationCommand(Command):
    """Commande pour retourner à la station précédente."""
    
    def __init__(self, navigator: StationNavigator):
        self.navigator = navigator
        
    def execute(self) -> bool:
        self.navigator.previous()
        return True
