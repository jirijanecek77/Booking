from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities import TimeSlot


class TimeSlotRepository(ABC):
    """Abstract repository interface for TimeSlot entity."""

    @abstractmethod
    async def create(self, time_slot: TimeSlot) -> TimeSlot:
        """Create a new time slot."""
        pass

    @abstractmethod
    async def get_by_id(self, slot_id: UUID) -> Optional[TimeSlot]:
        """Get time slot by ID."""
        pass

    @abstractmethod
    async def get_by_event_id(self, event_id: UUID) -> List[TimeSlot]:
        """Get all time slots for an event."""
        pass

    @abstractmethod
    async def update(self, time_slot: TimeSlot) -> TimeSlot:
        """Update a time slot."""
        pass

    @abstractmethod
    async def delete(self, slot_id: UUID) -> bool:
        """Delete a time slot."""
        pass
