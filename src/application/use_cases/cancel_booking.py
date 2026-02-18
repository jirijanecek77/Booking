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
        booking = await self.booking_repository.get_by_token(token)
        if not booking:
            return False

        session = getattr(self.booking_repository, "session", None)
        if session:
            async with session.begin():
                await self.time_slot_repository.release_spots(
                    booking.time_slot_id,
                    booking.number_of_seats,
                )
                return await self.booking_repository.delete(booking.id)

        await self.time_slot_repository.release_spots(
            booking.time_slot_id,
            booking.number_of_seats,
        )
        return await self.booking_repository.delete(booking.id)
