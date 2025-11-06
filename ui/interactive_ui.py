"""
Implémentation d'une interface utilisateur interactive et conversationnelle
pour la console, utilisant les bibliothèques `rich` et `questionary`.
"""
import questionary
import pandas as pd
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.rule import Rule
from interfaces.base_interfaces import UserInterface


class InteractiveConsoleUI(UserInterface):
    """
    Une interface utilisateur qui simule un chatbot dans la console.
    Elle utilise `questionary` pour les menus interactifs et `rich` pour un
    affichage stylisé.
    """

    def __init__(self):
        """Initialise la console `rich`."""
        self.console = Console()

    def display_message(self, message: str) -> None:
        """Affiche un message stylisé, comme si un bot parlait."""
        # On utilise la console `rich` pour un print avec des styles et emojis
        self.console.print(f"🤖 [Bot Météo] : {message}", style="italic cyan")

    def display_header(self, header: str) -> None:
        """Affiche un en-tête sous forme de règle horizontale stylisée."""
        # `Rule` de rich crée une ligne de séparation avec un titre
        self.console.print(Rule(f"[bold green]{header.upper()}", characters="─"))

    def prompt_for_choice(self, choices: List[str], prompt: str) -> Optional[str]:
        """
        Affiche un menu de sélection interactif (avec les flèches du clavier).
        """
        if not choices:
            self.display_message("Désolé, je n'ai trouvé aucune option disponible.")
            return None

        try:
            # `questionary.select` est la fonction clé qui crée le menu interactif.
            # L'utilisateur peut naviguer avec les flèches et appuyer sur Entrée.
            choice = questionary.select(
                message=prompt,
                choices=choices
            ).ask()  # .ask() lance le prompt et attend la réponse

            return choice

        except KeyboardInterrupt:
            # Sécurité supplémentaire si l'utilisateur quitte brutalement
            self.display_message("Sélection annulée.")
            return None

    def display_dataframe(self, df: pd.DataFrame, max_rows: int = 10) -> None:
        """Affiche les données d'un DataFrame dans un tableau bien formaté."""
        if df.empty:
            self.display_message("Aucune donnée à afficher.")
            return

        # On crée un objet Table de `rich`
        table = Table(
            title=f"Aperçu des Données ({len(df)} lignes)",
            show_header=True,
            header_style="bold magenta"
        )

        # On ajoute les colonnes au tableau en se basant sur le DataFrame
        for column in df.columns:
            table.add_column(column)

        # On ajoute les lignes au tableau
        df_head = df.head(max_rows)
        for _, row in df_head.iterrows():
            # On convertit chaque élément de la ligne en chaîne de caractères
            # L'étoile (*) dépaquette la liste pour l'envoyer comme arguments à add_row
            table.add_row(*[str(item) for item in row])

        self.console.print(table)