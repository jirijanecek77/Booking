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
        number_of_seats: int,
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
        # Basic validation and existence check
        time_slot = await self.time_slot_repository.get_by_id(time_slot_id)
        if not time_slot:
            raise ValueError("Time slot not found")

        if not time_slot.is_available(number_of_seats):
            raise ValueError("Time slot is full")

        booking = Booking(
            attendee_name=attendee_name,
            time_slot_id=time_slot_id,
            number_of_seats=number_of_seats,
            email=email,
        )

        session = getattr(self.booking_repository, "session", None)
        if session:
            async with session.begin():
                reserved = await self.time_slot_repository.reserve_spots(
                    time_slot_id,
                    number_of_seats,
                )
                if not reserved:
                    raise ValueError("Time slot is full")
                return await self.booking_repository.create(booking)

        reserved = await self.time_slot_repository.reserve_spots(time_slot_id, number_of_seats)
        if not reserved:
            raise ValueError("Time slot is full")
        return await self.booking_repository.create(booking)
