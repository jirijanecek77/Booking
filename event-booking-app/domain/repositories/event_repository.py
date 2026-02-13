from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from uuid import UUID

from domain.entities import Event


class EventRepository(ABC):
    """Abstract repository interface for Event entity."""

    @abstractmethod
    async def create(self, event: Event) -> Event:
        """Create a new event."""
        pass

    @abstractmethod
    async def get_by_id(self, event_id: UUID) -> Optional[Event]:
        """Get event by ID."""
        pass

    @abstractmethod
    async def get_all(self) -> List[Event]:
        """Get all events."""
        pass

    @abstractmethod
    async def get_by_date_range(self, start_date: date, end_date: date) -> List[Event]:
        """Get events within date range."""
        pass

    @abstractmethod
    async def update(self, event: Event) -> Event:
        """Update an event."""
        pass

    @abstractmethod
    async def delete(self, event_id: UUID) -> bool:
        """Delete an event."""
        pass
