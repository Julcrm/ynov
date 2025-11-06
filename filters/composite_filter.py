"""Filtre composite pour combiner plusieurs filtres"""
from interfaces.base_interfaces import DataFilter


class CompositeFilter(DataFilter):
    """Permet de combiner plusieurs filtres"""

    def __init__(self, filters):
        self.filters = filters

    def filter(self, df):
        result = df.copy()
        for current_filter in self.filters:
            result = current_filter.filter(result)
        return result