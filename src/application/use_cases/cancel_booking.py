from src.domain.repositories import BookingRepository, TimeSlotRepository


class CancelBookingUseCase:
    """Use case for canceling a booking."""

    def __init__(
        self,
        booking_repository: BookingRepository,
        time_slot_repository: TimeSlotRepository,
    ):
        self.booking_repository = booking_repository
        self.time_slot_repository = time_slot_repository

    async def execute(self, token: str) -> bool:
        """
        Cancel a booking.

        Args:
            token: Booking token

        Returns:
            True if canceled, False if not found
        """
        session = getattr(self.booking_repository, "session", None)
        if session:
            if session.in_transaction():
                return await self._cancel_booking(token)
            async with session.begin():
                return await self._cancel_booking(token)

        return await self._cancel_booking(token)

    async def _cancel_booking(self, token: str) -> bool:
        booking = await self.booking_repository.get_by_token(token)
        if not booking:
            return False

        await self.time_slot_repository.release_spots(
            booking.time_slot_id,
            booking.number_of_seats,
        )
        return await self.booking_repository.delete(booking.id)
