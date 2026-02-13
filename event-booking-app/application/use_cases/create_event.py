from datetime import date
from typing import List

from domain.entities import Event, TimeSlot
from domain.repositories import EventRepository, TimeSlotRepository


class CreateEventUseCase:
    """Use case for creating an event with time slots."""

    def __init__(
        self,
        event_repository: EventRepository,
        time_slot_repository: TimeSlotRepository,
    ):
        self.event_repository = event_repository
        self.time_slot_repository = time_slot_repository

    async def execute(
        self,
        name: str,
        event_date: date,
        time_slots: List[dict],
        description: str = None,
    ) -> Event:
        """
        Create a new event with time slots.

        Args:
            name: Event name
            event_date: Date of the event
            time_slots: List of dicts with start_time, end_time, max_capacity
            description: Optional event description

        Returns:
            Created Event entity
        """
        # Create event
        event = Event(name=name, event_date=event_date, description=description)
        created_event = await self.event_repository.create(event)

        # Create time slots
        for slot_data in time_slots:
            time_slot = TimeSlot(
                event_id=created_event.id,
                start_time=slot_data["start_time"],
                end_time=slot_data["end_time"],
                max_capacity=slot_data["max_capacity"],
            )
            created_slot = await self.time_slot_repository.create(time_slot)
            created_event.add_time_slot(created_slot)

        return created_event
