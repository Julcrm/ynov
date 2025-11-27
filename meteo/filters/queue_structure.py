""" Implémentation personnalisée d'une structure de données Queue (File FIFO). """
from typing import List, Any, Optional


class Queue:
    """
    Implémentation d'une file (Queue) utilisant le principe FIFO (First In, First Out).
    """

    def __init__(self):
        """
        Initialise une file vide.

        La file est implémentée avec une liste Python où:
        - Les éléments sont ajoutés à la FIN (append)
        - Les éléments sont retirés au DÉBUT (pop(0))
        """

        self._items: List[Any] = []

    def enqueue(self, item: Any) -> None:
        """
        Ajoute un élément à la fin de la file.

        Args:
            item: L'élément à ajouter à la file.

        Exemple:
            queue.enqueue("A")  # File: ["A"]
            queue.enqueue("B")  # File: ["A", "B"]
        """
        self._items.append(item)

    def dequeue(self) -> Any:
        """
        Retire et retourne le premier élément de la file.

        Returns:
            Le premier élément ajouté (principe FIFO).

        Raises:
            IndexError: Si la file est vide.

        Exemple:
            queue.enqueue("A")
            queue.enqueue("B")
            queue.dequeue()  # Retourne "A", File restante: ["B"]
        """
        if self.is_empty():
            raise IndexError("Impossible de retirer un élément d'une file vide")

        return self._items.pop(0)

    def peek(self) -> Optional[Any]:
        """
        Retourne le premier élément sans le retirer de la file.

        Returns:
            Le premier élément ou None si la file est vide.
        """
        if not self.is_empty():
            return self._items[0]
        return None

    def is_empty(self) -> bool:
        """
        Vérifie si la file est vide.

        Returns:
            bool: True si la file est vide, False sinon.
        """
        return len(self._items) == 0

    def size(self) -> int:
        """
        Retourne le nombre d'éléments dans la file.

        Returns:
            int: Le nombre d'éléments.
        """
        return len(self._items)

    def clear(self) -> None:
        """
        Vide complètement la file.
        """
        self._items = []

    def __str__(self) -> str:
        """
        Représentation textuelle de la file.

        Returns:
            str: La file sous forme de chaîne.
        """
        return f"Queue({self._items})"

    def __len__(self) -> int:
        """
        Permet d'utiliser len(queue) pour obtenir la taille.

        Returns:
            int: Le nombre d'éléments.
        """
        return self.size()
