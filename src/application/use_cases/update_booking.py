from uuid import UUID

from src.domain.entities import Booking
from src.domain.repositories import BookingRepository, TimeSlotRepository


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
        booking = await self.booking_repository.get_by_token(token)
        if not booking:
            raise ValueError("Booking not found")

        if booking.time_slot_id == new_time_slot_id:
            return booking

        new_slot = await self.time_slot_repository.get_by_id(new_time_slot_id)
        if not new_slot:
            raise ValueError("New time slot not found")

        if not new_slot.is_available(booking.number_of_seats):
            raise ValueError("New time slot is full")

        session = getattr(self.booking_repository, "session", None)
        if session:
            async with session.begin():
                reserved = await self.time_slot_repository.reserve_spots(
                    new_time_slot_id,
                    booking.number_of_seats,
                )
                if not reserved:
                    raise ValueError("New time slot is full")
                await self.time_slot_repository.release_spots(
                    booking.time_slot_id,
                    booking.number_of_seats,
                )
                booking.time_slot_id = new_time_slot_id
                return await self.booking_repository.update(booking)

        reserved = await self.time_slot_repository.reserve_spots(
            new_time_slot_id,
            booking.number_of_seats,
        )
        if not reserved:
            raise ValueError("New time slot is full")
        await self.time_slot_repository.release_spots(
            booking.time_slot_id,
            booking.number_of_seats,
        )
        booking.time_slot_id = new_time_slot_id
        return await self.booking_repository.update(booking)
