"""Service de haut niveau pour gérer les sélections de l'utilisateur."""
from typing import List, Optional
from ..interfaces.base_interfaces import UserInterface

class UserSelectionService:
    """
    Orchestre l'interaction avec l'utilisateur pour sélectionner un élément
    dans une liste, en utilisant un objet UI abstrait.
    """

    def __init__(self, ui: UserInterface):
        """
        Initialise le service avec une implémentation de l'interface utilisateur.

        Args:
            ui (UserInterface): L'objet qui gérera l'affichage et la saisie.
        """
        self.ui = ui

    def select_item_from_list(
        self,
        items: List[str],
        prompt: str,
        header: Optional[str] = None
    ) -> Optional[str]:
        """
        Affiche une liste d'éléments et demande à l'utilisateur d'en choisir un.

        Args:
            items (List[str]): La liste des choix à proposer.
            prompt (str): Le message invitant à la sélection.
            header (Optional[str], optional): Un titre à afficher avant la liste.

        Returns:
            Optional[str]: L'élément sélectionné par l'utilisateur
        """

        selected_item = self.ui.prompt_for_choice(items, prompt)

        if selected_item:
            self.ui.display_message(f"✓ Vous avez sélectionné : {selected_item}")

        return selected_item