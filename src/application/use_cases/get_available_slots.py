from typing import List
from uuid import UUID

from src.domain.entities import TimeSlot
from src.domain.repositories import TimeSlotRepository


class GetAvailableSlotsUseCase:
    """Use case for retrieving available time slots for an event."""

    def __init__(self, time_slot_repository: TimeSlotRepository):
        self.time_slot_repository = time_slot_repository

    async def execute(self, event_id: UUID) -> List[TimeSlot]:
        """
        Get all available time slots for an event.

        Args:
            event_id: Event ID

        Returns:
            List of TimeSlot entities with availability info
        """
        slots = await self.time_slot_repository.get_by_event_id(event_id)
        return slots
