from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.entities import Event, TimeSlot, Booking
from src.domain.repositories import EventRepository, TimeSlotRepository, BookingRepository
from .models import EventModel, TimeSlotModel, BookingModel


class SQLAlchemyEventRepository(EventRepository):
    """SQLAlchemy implementation of EventRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: EventModel) -> Event:
        """Convert model to entity."""
        event = Event(
            name=model.name,
            event_date=model.event_date,
            description=model.description,
            event_id=model.id,
        )
        for slot_model in model.time_slots:
            slot = TimeSlot(
                event_id=slot_model.event_id,
                start_time=slot_model.start_time,
                end_time=slot_model.end_time,
                max_capacity=slot_model.max_capacity,
                current_bookings=slot_model.current_bookings,
                slot_id=slot_model.id,
            )
            event.add_time_slot(slot)
        return event

    def _to_model(self, entity: Event) -> EventModel:
        """Convert entity to model."""
        return EventModel(
            id=entity.id,
            name=entity.name,
            event_date=entity.event_date,
            description=entity.description,
        )

    async def create(self, event: Event) -> Event:
        model = self._to_model(event)
        self.session.add(model)
        if self.session.in_transaction():
            await self.session.flush()
        else:
            await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, event_id: UUID) -> Optional[Event]:
        stmt = (
            select(EventModel)
            .where(EventModel.id == event_id)
            .options(selectinload(EventModel.time_slots))
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self) -> List[Event]:
        stmt = select(EventModel).options(selectinload(EventModel.time_slots))
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def get_by_date_range(self, start_date: date, end_date: date) -> List[Event]:
        stmt = (
            select(EventModel)
            .where(EventModel.event_date >= start_date, EventModel.event_date <= end_date)
            .options(selectinload(EventModel.time_slots))
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def update(self, event: Event) -> Event:
        stmt = select(EventModel).where(EventModel.id == event.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            model.name = event.name
            model.event_date = event.event_date
            model.description = event.description
            if self.session.in_transaction():
                await self.session.flush()
            else:
                await self.session.commit()
            await self.session.refresh(model)
            return self._to_entity(model)
        raise ValueError("Event not found")

    async def delete(self, event_id: UUID) -> bool:
        stmt = select(EventModel).where(EventModel.id == event_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            if self.session.in_transaction():
                await self.session.flush()
            else:
                await self.session.commit()
            return True
        return False


class SQLAlchemyTimeSlotRepository(TimeSlotRepository):
    """SQLAlchemy implementation of TimeSlotRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: TimeSlotModel) -> TimeSlot:
        """Convert model to entity."""
        return TimeSlot(
            event_id=model.event_id,
            start_time=model.start_time,
            end_time=model.end_time,
            max_capacity=model.max_capacity,
            current_bookings=model.current_bookings,
            slot_id=model.id,
        )

    def _to_model(self, entity: TimeSlot) -> TimeSlotModel:
        """Convert entity to model."""
        return TimeSlotModel(
            id=entity.id,
            event_id=entity.event_id,
            start_time=entity.start_time,
            end_time=entity.end_time,
            max_capacity=entity.max_capacity,
            current_bookings=entity.current_bookings,
        )

    async def create(self, time_slot: TimeSlot) -> TimeSlot:
        model = self._to_model(time_slot)
        self.session.add(model)
        if self.session.in_transaction():
            await self.session.flush()
        else:
            await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, slot_id: UUID) -> Optional[TimeSlot]:
        stmt = select(TimeSlotModel).where(TimeSlotModel.id == slot_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_event_id(self, event_id: UUID) -> List[TimeSlot]:
        stmt = select(TimeSlotModel).where(TimeSlotModel.event_id == event_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def update(self, time_slot: TimeSlot) -> TimeSlot:
        stmt = select(TimeSlotModel).where(TimeSlotModel.id == time_slot.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            model.start_time = time_slot.start_time
            model.end_time = time_slot.end_time
            model.max_capacity = time_slot.max_capacity
            model.current_bookings = time_slot.current_bookings
            if self.session.in_transaction():
                await self.session.flush()
            else:
                await self.session.commit()
            await self.session.refresh(model)
            return self._to_entity(model)
        raise ValueError("TimeSlot not found")

    async def reserve_spots(self, slot_id: UUID, seats: int) -> bool:
        if seats <= 0:
            return False
        stmt = (
            update(TimeSlotModel)
            .where(TimeSlotModel.id == slot_id)
            .where(TimeSlotModel.current_bookings + seats <= TimeSlotModel.max_capacity)
            .values(current_bookings=TimeSlotModel.current_bookings + seats)
        )
        result = await self.session.execute(stmt)
        if self.session.in_transaction():
            await self.session.flush()
        else:
            await self.session.commit()
        return result.rowcount == 1

    async def release_spots(self, slot_id: UUID, seats: int) -> None:
        if seats <= 0:
            return
        stmt = (
            update(TimeSlotModel)
            .where(TimeSlotModel.id == slot_id)
            .where(TimeSlotModel.current_bookings - seats >= 0)
            .values(current_bookings=TimeSlotModel.current_bookings - seats)
        )
        await self.session.execute(stmt)
        if self.session.in_transaction():
            await self.session.flush()
        else:
            await self.session.commit()

    async def delete(self, slot_id: UUID) -> bool:
        stmt = select(TimeSlotModel).where(TimeSlotModel.id == slot_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            if self.session.in_transaction():
                await self.session.flush()
            else:
                await self.session.commit()
            return True
        return False


class SQLAlchemyBookingRepository(BookingRepository):
    """SQLAlchemy implementation of BookingRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: BookingModel) -> Booking:
        """Convert model to entity."""
        return Booking(
            attendee_name=model.attendee_name,
            time_slot_id=model.time_slot_id,
            number_of_seats=model.number_of_seats,
            booking_token=model.booking_token,
            booking_id=model.id,
            created_at=model.created_at,
            email=model.email,
        )

    def _to_model(self, entity: Booking) -> BookingModel:
        """Convert entity to model."""
        return BookingModel(
            id=entity.id,
            attendee_name=entity.attendee_name,
            time_slot_id=entity.time_slot_id,
            number_of_seats=entity.number_of_seats,
            booking_token=entity.booking_token,
            email=entity.email,
            created_at=entity.created_at,
        )

    async def create(self, booking: Booking) -> Booking:
        model = self._to_model(booking)
        self.session.add(model)
        if self.session.in_transaction():
            await self.session.flush()
        else:
            await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, booking_id: UUID) -> Optional[Booking]:
        stmt = select(BookingModel).where(BookingModel.id == booking_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_token(self, token: str) -> Optional[Booking]:
        stmt = select(BookingModel).where(BookingModel.booking_token == token)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_time_slot_id(self, time_slot_id: UUID) -> List[Booking]:
        stmt = select(BookingModel).where(BookingModel.time_slot_id == time_slot_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def update(self, booking: Booking) -> Booking:
        stmt = select(BookingModel).where(BookingModel.id == booking.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            model.attendee_name = booking.attendee_name
            model.time_slot_id = booking.time_slot_id
            model.number_of_seats = booking.number_of_seats
            model.email = booking.email
            if self.session.in_transaction():
                await self.session.flush()
            else:
                await self.session.commit()
            await self.session.refresh(model)
            return self._to_entity(model)
        raise ValueError("Booking not found")

    async def delete(self, booking_id: UUID) -> bool:
        stmt = select(BookingModel).where(BookingModel.id == booking_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            if self.session.in_transaction():
                await self.session.flush()
            else:
                await self.session.commit()
            return True
        return False
