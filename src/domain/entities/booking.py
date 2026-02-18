from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
import secrets


class Booking:
    """Domain entity representing a booking."""

    def __init__(
        self,
        attendee_name: str,
        time_slot_id: UUID,
        number_of_seats: int = 1,
        booking_token: Optional[str] = None,
        booking_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        email: Optional[str] = None,
    ):
        self.id = booking_id or uuid4()
        self.attendee_name = attendee_name
        self.time_slot_id = time_slot_id
        self.number_of_seats = number_of_seats
        self.booking_token = booking_token or self._generate_token()
        self.created_at = created_at or datetime.utcnow()
        self.email = email  # Optional for notifications

    @staticmethod
    def _generate_token() -> str:
        """Generate a secure random token for booking management."""
        return secrets.token_urlsafe(32)

    def __repr__(self) -> str:
        return f"Booking(id={self.id}, name={self.attendee_name}, token={self.booking_token[:8]}...)"
