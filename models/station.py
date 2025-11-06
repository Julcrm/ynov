"""Modèle de données pour une station météo"""


class Station:
    """Représente une station météo"""
    def __init__(self, dataset_id, creator):
        self.dataset_id = dataset_id
        self.creator = creator