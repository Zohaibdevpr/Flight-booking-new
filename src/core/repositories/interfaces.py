"""
Repository interface.

DIP: Abstract interface for all repositories.
Different storage implementations depend on this abstraction.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class Repository(ABC):
    """
    DIP: Generic repository interface.

    This interface defines the contract for data persistence.
    High-level modules depend on this abstraction, not specific storage implementations.
    """

    @abstractmethod
    def add(self, entity_id: str, entity: Any) -> bool:
        """
        Add an entity to the repository.

        Args:
            entity_id: Unique identifier for the entity
            entity: Entity object to store

        Returns:
            True if entity was added successfully
        """
        pass

    @abstractmethod
    def get(self, entity_id: str) -> Optional[Any]:
        """
        Retrieve an entity by ID.

        Args:
            entity_id: Unique identifier for the entity

        Returns:
            Entity object or None if not found
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Any]:
        """
        Retrieve all entities.

        Returns:
            List of all entities
        """
        pass

    @abstractmethod
    def update(self, entity_id: str, entity: Any) -> bool:
        """
        Update an existing entity.

        Args:
            entity_id: Unique identifier for the entity
            entity: Updated entity object

        Returns:
            True if entity was updated successfully
        """
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Delete an entity.

        Args:
            entity_id: Unique identifier for the entity

        Returns:
            True if entity was deleted successfully
        """
        pass

    @abstractmethod
    def exists(self, entity_id: str) -> bool:
        """
        Check if an entity exists.

        Args:
            entity_id: Unique identifier for the entity

        Returns:
            True if entity exists
        """
        pass
