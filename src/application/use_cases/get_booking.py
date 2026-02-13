from typing import Optional

from src.domain.entities import Booking
from src.domain.repositories import BookingRepository


class GetBookingUseCase:
    """Use case for retrieving a booking by token."""

    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    async def execute(self, token: str) -> Optional[Booking]:
        """
        Get booking by token.

        Args:
            token: Booking token

        Returns:
            Booking entity if found, None otherwise
        """
        return await self.booking_repository.get_by_token(token)
