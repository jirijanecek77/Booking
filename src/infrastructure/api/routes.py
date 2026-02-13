from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases.cancel_booking import CancelBookingUseCase
from src.application.use_cases.create_booking import CreateBookingUseCase
from src.application.use_cases.create_event import CreateEventUseCase
from src.application.use_cases.get_available_slots import GetAvailableSlotsUseCase
from src.application.use_cases.get_booking import GetBookingUseCase
from src.application.use_cases.update_booking import UpdateBookingUseCase
from src.infrastructure.database import get_db
from src.infrastructure.database.repositories import (
    SQLAlchemyEventRepository,
    SQLAlchemyTimeSlotRepository,
    SQLAlchemyBookingRepository,
)
from .schemas import (
    EventCreate,
    EventResponse,
    BookingCreate,
    BookingResponse,
    BookingUpdate,
    TimeSlotResponse,
)

router = APIRouter()


# Event endpoints
@router.post("/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(event_data: EventCreate, db: AsyncSession = Depends(get_db)):
    """Create a new event with time slots."""
    event_repo = SQLAlchemyEventRepository(db)
    time_slot_repo = SQLAlchemyTimeSlotRepository(db)
    use_case = CreateEventUseCase(event_repo, time_slot_repo)

    try:
        time_slots = [slot.model_dump() for slot in event_data.time_slots]
        event = await use_case.execute(
            name=event_data.name,
            event_date=event_data.event_date,
            time_slots=time_slots,
            description=event_data.description,
        )

        return EventResponse(
            id=event.id,
            name=event.name,
            event_date=event.event_date,
            description=event.description,
            time_slots=[
                TimeSlotResponse(
                    id=slot.id,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    max_capacity=slot.max_capacity,
                    current_bookings=slot.current_bookings,
                    available_spots=slot.available_spots(),
                )
                for slot in event.time_slots
            ],
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/events", response_model=List[EventResponse])
async def get_all_events(db: AsyncSession = Depends(get_db)):
    """Get all events."""
    event_repo = SQLAlchemyEventRepository(db)
    events = await event_repo.get_all()

    return [
        EventResponse(
            id=event.id,
            name=event.name,
            event_date=event.event_date,
            description=event.description,
            time_slots=[
                TimeSlotResponse(
                    id=slot.id,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    max_capacity=slot.max_capacity,
                    current_bookings=slot.current_bookings,
                    available_spots=slot.available_spots(),
                )
                for slot in event.time_slots
            ],
        )
        for event in events
    ]


@router.get("/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get event by ID."""
    event_repo = SQLAlchemyEventRepository(db)
    event = await event_repo.get_by_id(event_id)

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    return EventResponse(
        id=event.id,
        name=event.name,
        event_date=event.event_date,
        description=event.description,
        time_slots=[
            TimeSlotResponse(
                id=slot.id,
                start_time=slot.start_time,
                end_time=slot.end_time,
                max_capacity=slot.max_capacity,
                current_bookings=slot.current_bookings,
                available_spots=slot.available_spots(),
            )
            for slot in event.time_slots
        ],
    )


@router.get("/events/{event_id}/slots", response_model=List[TimeSlotResponse])
async def get_event_slots(event_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get available time slots for an event."""
    time_slot_repo = SQLAlchemyTimeSlotRepository(db)
    use_case = GetAvailableSlotsUseCase(time_slot_repo)

    slots = await use_case.execute(event_id)

    return [
        TimeSlotResponse(
            id=slot.id,
            start_time=slot.start_time,
            end_time=slot.end_time,
            max_capacity=slot.max_capacity,
            current_bookings=slot.current_bookings,
            available_spots=slot.available_spots(),
        )
        for slot in slots
    ]


# Booking endpoints
@router.post("/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(booking_data: BookingCreate, db: AsyncSession = Depends(get_db)):
    """Create a new booking."""
    booking_repo = SQLAlchemyBookingRepository(db)
    time_slot_repo = SQLAlchemyTimeSlotRepository(db)
    use_case = CreateBookingUseCase(booking_repo, time_slot_repo)

    try:
        booking = await use_case.execute(
            attendee_name=booking_data.attendee_name,
            time_slot_id=booking_data.time_slot_id,
            email=booking_data.email,
        )

        return BookingResponse(
            id=booking.id,
            attendee_name=booking.attendee_name,
            time_slot_id=booking.time_slot_id,
            booking_token=booking.booking_token,
            email=booking.email,
            created_at=booking.created_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/bookings/{token}", response_model=BookingResponse)
async def get_booking(token: str, db: AsyncSession = Depends(get_db)):
    """Get booking by token."""
    booking_repo = SQLAlchemyBookingRepository(db)
    use_case = GetBookingUseCase(booking_repo)

    booking = await use_case.execute(token)

    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    return BookingResponse(
        id=booking.id,
        attendee_name=booking.attendee_name,
        time_slot_id=booking.time_slot_id,
        booking_token=booking.booking_token,
        email=booking.email,
        created_at=booking.created_at,
    )


@router.put("/bookings/{token}", response_model=BookingResponse)
async def update_booking(
    token: str, booking_update: BookingUpdate, db: AsyncSession = Depends(get_db)
):
    """Update booking to a new time slot."""
    booking_repo = SQLAlchemyBookingRepository(db)
    time_slot_repo = SQLAlchemyTimeSlotRepository(db)
    use_case = UpdateBookingUseCase(booking_repo, time_slot_repo)

    try:
        booking = await use_case.execute(token, booking_update.new_time_slot_id)

        return BookingResponse(
            id=booking.id,
            attendee_name=booking.attendee_name,
            time_slot_id=booking.time_slot_id,
            booking_token=booking.booking_token,
            email=booking.email,
            created_at=booking.created_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/bookings/{token}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_booking(token: str, db: AsyncSession = Depends(get_db)):
    """Cancel a booking."""
    booking_repo = SQLAlchemyBookingRepository(db)
    time_slot_repo = SQLAlchemyTimeSlotRepository(db)
    use_case = CancelBookingUseCase(booking_repo, time_slot_repo)

    success = await use_case.execute(token)

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
