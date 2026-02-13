from uuid import UUID

from domain.entities import Booking
from domain.repositories import BookingRepository, TimeSlotRepository


class UpdateBookingUseCase:
    """Use case for updating a booking (changing time slot)."""

    def __init__(
        self,
        booking_repository: BookingRepository,
        time_slot_repository: TimeSlotRepository,
    ):
        self.booking_repository = booking_repository
        self.time_slot_repository = time_slot_repository

    async def execute(self, token: str, new_time_slot_id: UUID) -> Booking:
        """
        Update booking to a new time slot.

        Args:
            token: Booking token
            new_time_slot_id: New time slot ID

        Returns:
            Updated Booking entity

        Raises:
            ValueError: If booking not found or new slot is full
        """
        # Get existing booking
        booking = await self.booking_repository.get_by_token(token)
        if not booking:
            raise ValueError("Booking not found")

        # Get old and new time slots
        old_slot = await self.time_slot_repository.get_by_id(booking.time_slot_id)
        new_slot = await self.time_slot_repository.get_by_id(new_time_slot_id)

        if not new_slot:
            raise ValueError("New time slot not found")

        if not new_slot.is_available():
            raise ValueError("New time slot is full")

        # Update capacities
        if old_slot:
            old_slot.decrement_bookings()
            await self.time_slot_repository.update(old_slot)

        new_slot.increment_bookings()
        await self.time_slot_repository.update(new_slot)

        # Update booking
        booking.time_slot_id = new_time_slot_id
        return await self.booking_repository.update(booking)
