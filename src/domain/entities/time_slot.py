from datetime import time
from typing import Optional
from uuid import UUID, uuid4


class TimeSlot:
    """Domain entity representing a time slot for bookings."""

    def __init__(
        self,
        event_id: UUID,
        start_time: time,
        end_time: time,
        max_capacity: int,
        current_bookings: int = 0,
        slot_id: Optional[UUID] = None,
    ):
        self.id = slot_id or uuid4()
        self.event_id = event_id
        self.start_time = start_time
        self.end_time = end_time
        self.max_capacity = max_capacity
        self.current_bookings = current_bookings

    def is_available(self) -> bool:
        """Check if slot has available capacity."""
        return self.current_bookings < self.max_capacity

    def increment_bookings(self) -> None:
        """Increment booking count."""
        if not self.is_available():
            raise ValueError("Time slot is full")
        self.current_bookings += 1

    def decrement_bookings(self) -> None:
        """Decrement booking count."""
        if self.current_bookings > 0:
            self.current_bookings -= 1

    def available_spots(self) -> int:
        """Get number of available spots."""
        return self.max_capacity - self.current_bookings

    def __repr__(self) -> str:
        return f"TimeSlot(id={self.id}, start={self.start_time}, capacity={self.current_bookings}/{self.max_capacity})"
