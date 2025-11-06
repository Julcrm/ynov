"""Service de sélection utilisateur"""


class UserSelectionService:
    """
    Responsabilité unique: Gérer l'interaction de sélection avec l'utilisateur
    """

    def __init__(self, ui):
        self.ui = ui

    def select_item_from_list(self, items, prompt, header=None):
        """
        Demande à l'utilisateur de sélectionner un élément dans une liste
        Retourne l'élément sélectionné ou None
        """
        if header:
            self.ui.display_header(header)

        selected = self.ui.prompt_for_choice(items, prompt)

        if selected:
            self.ui.display_message(f"✓ Sélectionné : {selected}")

        return selected