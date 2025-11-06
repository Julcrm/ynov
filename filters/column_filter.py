"""Filtre pour sélectionner certaines colonnes"""
import pandas as pd
from interfaces.base_interfaces import DataFilter


class ColumnFilter(DataFilter):
    """Filtre pour sélectionner uniquement certaines colonnes utiles."""

    def __init__(self):
        self.columns_to_keep = ["heure_de_paris", "temperature_en_degre_c", "humidite", "pression"]

    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            print("⚠ Le DataFrame est vide — aucune colonne à filtrer.")
            return df

        existing_columns = [col for col in self.columns_to_keep if col in df.columns]

        if not existing_columns:
            print("⚠ Aucune des colonnes définies n'existe dans les données.")

        return df[existing_columns].copy()