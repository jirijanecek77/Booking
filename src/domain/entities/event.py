from datetime import date
from typing import List, Optional
from uuid import UUID, uuid4


class Event:
    """Domain entity representing an event."""

    def __init__(
        self,
        name: str,
        event_date: date,
        description: Optional[str] = None,
        event_id: Optional[UUID] = None,
    ):
        self.id = event_id or uuid4()
        self.name = name
        self.event_date = event_date
        self.description = description
        self.time_slots: List["TimeSlot"] = []

    def add_time_slot(self, time_slot: "TimeSlot") -> None:
        """Add a time slot to the event."""
        self.time_slots.append(time_slot)

    def __repr__(self) -> str:
        return f"Event(id={self.id}, name={self.name}, date={self.event_date})"
