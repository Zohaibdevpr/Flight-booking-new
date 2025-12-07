"""
Repository pattern implementation.

DIP: Repository pattern abstracts data persistence, allowing the business logic
to depend on abstractions rather than concrete data storage implementations.
"""

from .interfaces import Repository
from .in_memory_repo import InMemoryRepository

__all__ = [
    "Repository",
    "InMemoryRepository",
]
