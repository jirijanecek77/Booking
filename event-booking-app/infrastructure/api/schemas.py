from datetime import date, time, datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class TimeSlotCreate(BaseModel):
    start_time: time
    end_time: time
    max_capacity: int = Field(gt=0)


class TimeSlotResponse(BaseModel):
    id: UUID
    start_time: time
    end_time: time
    max_capacity: int
    current_bookings: int
    available_spots: int

    class Config:
        from_attributes = True


class EventCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    event_date: date
    description: Optional[str] = None
    time_slots: List[TimeSlotCreate]


class EventResponse(BaseModel):
    id: UUID
    name: str
    event_date: date
    description: Optional[str]
    time_slots: List[TimeSlotResponse] = []

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    attendee_name: str = Field(min_length=1, max_length=255)
    time_slot_id: UUID
    email: Optional[str] = None


class BookingResponse(BaseModel):
    id: UUID
    attendee_name: str
    time_slot_id: UUID
    booking_token: str
    email: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class BookingUpdate(BaseModel):
    new_time_slot_id: UUID
