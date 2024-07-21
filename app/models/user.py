from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from ..db.base import Base
from datetime import datetime
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    tickets = relationship("Ticket", back_populates="customer")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    place = Column(String, nullable=False)
    city = Column(String, nullable=False)
    hotel = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    tm_created = Column(DateTime, default=datetime.utcnow)
    tm_updated = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    customer_id = Column(Integer, ForeignKey("users.id"))
    customer = relationship("User", back_populates="tickets")
