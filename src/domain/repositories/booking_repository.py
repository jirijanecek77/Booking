from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities import Booking


class BookingRepository(ABC):
    """Abstract repository interface for Booking entity."""

    @abstractmethod
    async def create(self, booking: Booking) -> Booking:
        """Create a new booking."""
        pass

    @abstractmethod
    async def get_by_id(self, booking_id: UUID) -> Optional[Booking]:
        """Get booking by ID."""
        pass

    @abstractmethod
    async def get_by_token(self, token: str) -> Optional[Booking]:
        """Get booking by token."""
        pass

    @abstractmethod
    async def get_by_time_slot_id(self, time_slot_id: UUID) -> List[Booking]:
        """Get all bookings for a time slot."""
        pass

    @abstractmethod
    async def update(self, booking: Booking) -> Booking:
        """Update a booking."""
        pass

    @abstractmethod
    async def delete(self, booking_id: UUID) -> bool:
        """Delete a booking."""
        pass
