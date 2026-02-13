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
        # Get booking
        booking = await self.booking_repository.get_by_token(token)
        if not booking:
            return False

        # Update slot capacity
        time_slot = await self.time_slot_repository.get_by_id(booking.time_slot_id)
        if time_slot:
            time_slot.decrement_bookings()
            await self.time_slot_repository.update(time_slot)

        # Delete booking
        return await self.booking_repository.delete(booking.id)
