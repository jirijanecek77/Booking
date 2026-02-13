from typing import Optional
from uuid import UUID

from src.domain.entities import Booking
from src.domain.repositories import BookingRepository, TimeSlotRepository


class CreateBookingUseCase:
    """Use case for creating a booking."""

    def __init__(
        self,
        booking_repository: BookingRepository,
        time_slot_repository: TimeSlotRepository,
    ):
        self.booking_repository = booking_repository
        self.time_slot_repository = time_slot_repository

    async def execute(
        self,
        attendee_name: str,
        time_slot_id: UUID,
        email: Optional[str] = None,
    ) -> Booking:
        """
        Create a new booking.

        Args:
            attendee_name: Name of the attendee
            time_slot_id: ID of the time slot to book
            email: Optional email for notifications

        Returns:
            Created Booking entity with token

        Raises:
            ValueError: If time slot is full or doesn't exist
        """
        # Get time slot
        time_slot = await self.time_slot_repository.get_by_id(time_slot_id)
        if not time_slot:
            raise ValueError("Time slot not found")

        # Check availability
        if not time_slot.is_available():
            raise ValueError("Time slot is full")

        # Create booking
        booking = Booking(
            attendee_name=attendee_name,
            time_slot_id=time_slot_id,
            email=email,
        )
        created_booking = await self.booking_repository.create(booking)

        # Update slot capacity
        time_slot.increment_bookings()
        await self.time_slot_repository.update(time_slot)

        return created_booking
