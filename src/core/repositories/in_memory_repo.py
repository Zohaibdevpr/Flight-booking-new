"""
In-memory repository implementation.

DIP: Concrete implementation of Repository using in-memory storage.
"""

from typing import Any, List, Optional
from .interfaces import Repository


class InMemoryRepository(Repository):
    """
    DIP: In-memory repository implementation.

    This implementation stores entities in memory while depending on
    the Repository abstraction. Useful for testing and simple applications.
    """

    def __init__(self):
        """Initialize in-memory repository."""
        self._storage = {}

    def add(self, entity_id: str, entity: Any) -> bool:
        """
        Add an entity to the repository.

        Args:
            entity_id: Unique identifier for the entity
            entity: Entity object to store

        Returns:
            True if entity was added successfully
        """
        if not entity_id:
            raise ValueError("Entity ID cannot be empty")

        if entity_id in self._storage:
            raise ValueError(f"Entity with ID '{entity_id}' already exists")

        self._storage[entity_id] = entity
        return True

    def get(self, entity_id: str) -> Optional[Any]:
        """
        Retrieve an entity by ID.

        Args:
            entity_id: Unique identifier for the entity

        Returns:
            Entity object or None if not found
        """
        return self._storage.get(entity_id)

    def get_all(self) -> List[Any]:
        """
        Retrieve all entities.

        Returns:
            List of all entities
        """
        return list(self._storage.values())

    def update(self, entity_id: str, entity: Any) -> bool:
        """
        Update an existing entity.

        Args:
            entity_id: Unique identifier for the entity
            entity: Updated entity object

        Returns:
            True if entity was updated successfully
        """
        if entity_id not in self._storage:
            raise ValueError(f"Entity with ID '{entity_id}' not found")

        self._storage[entity_id] = entity
        return True

    def delete(self, entity_id: str) -> bool:
        """
        Delete an entity.

        Args:
            entity_id: Unique identifier for the entity

        Returns:
            True if entity was deleted successfully
        """
        if entity_id not in self._storage:
            raise ValueError(f"Entity with ID '{entity_id}' not found")

        del self._storage[entity_id]
        return True

    def exists(self, entity_id: str) -> bool:
        """
        Check if an entity exists.

        Args:
            entity_id: Unique identifier for the entity

        Returns:
            True if entity exists
        """
        return entity_id in self._storage

    def count(self) -> int:
        """
        Get number of entities in repository.

        Returns:
            Number of stored entities
        """
        return len(self._storage)

    def clear(self) -> None:
        """Clear all entities from repository."""
        self._storage.clear()
