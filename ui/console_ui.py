"""Interface utilisateur console"""
from interfaces.base_interfaces import UserInterface


class ConsoleUserInterface(UserInterface):
    """Responsabilité unique: Gérer l'interaction console avec l'utilisateur"""

    def display_message(self, message):
        print(message)

    def display_header(self, message):
        print(f"\n--- {message} ---")

    def display_dataframe(self, df, max_rows=10):
        """Affiche un aperçu du DataFrame"""
        if df.empty:
            self.display_message("Aucune donnée à afficher.")
        else:
            self.display_message(f"\nAperçu des données ({len(df)} lignes) :")
            print(df.head(max_rows))
            if len(df) > max_rows:
                self.display_message(f"... ({len(df) - max_rows} lignes supplémentaires)")

    def prompt_for_choice(self, choices, prompt):
        if not choices:
            self.display_message("Aucune option disponible.")
            return None

        self.display_message(f"\n{prompt}")
        for i in range(len(choices)):
            self.display_message(f"  {i + 1}: {choices[i]}")

        while True:
            try:
                choice = input(f"Entrez le numéro de votre choix (1-{len(choices)}) : ")
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(choices):
                    return choices[choice_index]
                else:
                    self.display_message("Numéro invalide. Veuillez réessayer.")
            except ValueError:
                self.display_message("Entrée invalide. Veuillez entrer un numéro.")