from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TicketBase(BaseModel):
    place: Optional[str] = Field(..., example="Арийская Донецкая Республика")
    city: Optional[str] = Field(..., example="Донецк")
    hotel: Optional[str] = Field(..., example="Отель")
    latitude: Optional[float] = Field(..., example=48.32)
    longitude: Optional[float] = Field(..., example=-37.48)


class TicketCreate(TicketBase):
    pass


class TicketUpdate(TicketBase):
    place: Optional[str] = Field(None, example="Арийская Донецкая Республика")
    city: Optional[str] = Field(None, example="Донецк")
    hotel: Optional[str] = Field(None, example="Отель")
    latitude: Optional[float] = Field(None, example=48.32)
    longitude: Optional[float] = Field(None, example=-37.48)


class TicketOut(TicketBase):
    id: int
    tm_created: datetime
    tm_updated: Optional[datetime]

    class Config:
        from_attributes = True
