"""Implémentation console de l'interface utilisateur."""
import pandas as pd
from typing import List, Optional
from interfaces.base_interfaces import UserInterface


class ConsoleUserInterface(UserInterface):
    """Gère toutes les interactions (entrées/sorties) via la console."""

    def display_message(self, message: str) -> None:
        """Affiche un message simple."""
        print(message)

    def display_header(self, header: str) -> None:
        """Affiche un en-tête pour structurer la sortie."""
        print(f"\n--- {header.upper()} ---")

    def display_dataframe(self, df: pd.DataFrame, max_rows: int = 10) -> None:
        """Affiche un aperçu formaté d'un DataFrame."""
        if df.empty:
            self.display_message("Aucune donnée à afficher.")
            return

        self.display_message(f"\nAperçu des données ({len(df)} lignes totales) :")
        print(df.head(max_rows).to_string())
        
        if len(df) > max_rows:
            self.display_message(f"... et {len(df) - max_rows} autres lignes.")

    def prompt_for_choice(self, choices: List[str], prompt: str) -> Optional[str]:
        """Propose une liste de choix numérotés et retourne la sélection."""
        if not choices:
            self.display_message("Aucune option disponible pour la sélection.")
            return None

        self.display_message(f"\n{prompt}")

        for i, choice in enumerate(choices, start=1):
            self.display_message(f"  {i}: {choice}")

        num_choices = len(choices)
        while True:
            try:
                user_input = input(f"Entrez le numéro de votre choix (1-{num_choices}) : ")
                if not user_input:

                    return None
                
                choice_index = int(user_input) - 1
                
                if 0 <= choice_index < num_choices:
                    return choices[choice_index]
                else:
                    self.display_message(f"Numéro invalide. Il doit être entre 1 et {num_choices}.")
            
            except ValueError:
                self.display_message("Entrée invalide. Veuillez entrer un numéro.")
            except (KeyboardInterrupt, EOFError):

                self.display_message("\nSélection annulée. Au revoir !")
                return None