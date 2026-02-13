from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, Time, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import uuid

from .database import Base


class EventModel(Base):
    __tablename__ = "events"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    event_date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)

    time_slots = relationship("TimeSlotModel", back_populates="event", cascade="all, delete-orphan")


class TimeSlotModel(Base):
    __tablename__ = "time_slots"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(PGUUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    max_capacity = Column(Integer, nullable=False)
    current_bookings = Column(Integer, default=0)

    event = relationship("EventModel", back_populates="time_slots")
    bookings = relationship("BookingModel", back_populates="time_slot", cascade="all, delete-orphan")


class BookingModel(Base):
    __tablename__ = "bookings"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attendee_name = Column(String(255), nullable=False)
    time_slot_id = Column(PGUUID(as_uuid=True), ForeignKey("time_slots.id"), nullable=False)
    booking_token = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    time_slot = relationship("TimeSlotModel", back_populates="bookings")
