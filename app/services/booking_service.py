from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.user import *
from ..models.user import Ticket
from ..schemas.booking import TicketCreate, TicketUpdate
from typing import List, Sequence, Dict, Tuple
from fastapi import HTTPException, status


async def create_ticket(ticket: TicketCreate, db: AsyncSession, current_user: User) -> Ticket:
    """
    Creates a new ticket for a customer.
    :param ticket:
    :param db:
    :param current_user:
    :return:
    """
    new_ticket = Ticket(**ticket.dict(), customer_id=current_user.id)

    db.add(new_ticket)
    await db.commit()

    return new_ticket


async def get_all_tickets(db: AsyncSession, current_user: User) -> Sequence[Ticket]:  # List[Ticket]
    """
    Gets all tickets for a customer.
    :param db:
    :param current_user:
    :return:
    """
    result = await db.execute(select(Ticket).where(current_user.id == Ticket.customer_id))
    tickets = result.scalars().all()
    return tickets


async def get_ticket(ticket_id: int, db: AsyncSession, current_user: User) -> Ticket:
    """
    Gets a single ticket for a customer by its ID.
    :param ticket_id:
    :param db:
    :param current_user:
    :return:
    """
    result = await db.execute(select(Ticket).where(ticket_id == Ticket.id, current_user.id == Ticket.customer_id))
    ticket = result.scalars().first()
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return ticket


async def update_ticket(
        ticket_id: int,
        ticket_update:
        TicketUpdate,
        db: AsyncSession,
        current_user: User) \
    -> Ticket:

    """
    Updates an existing ticket for a customer.
    :param ticket_id:
    :param ticket_update:
    :param db:
    :param current_user:
    :return:
    """
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id, Ticket.customer_id == current_user.id))
    ticket = result.scalars().first()
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    for key, value in ticket_update.dict(exclude_unset=True).items():
        setattr(ticket, key, value)

    await db.commit()

    return ticket


async def delete_ticket(ticket_id: int, db: AsyncSession, current_user: User):
    """
    Deletes a ticket for a customer by its ID.
    :param ticket_id:
    :param db:
    :param current_user:
    :return:
    """
    result = await db.execute(select(Ticket).where(ticket_id == Ticket.id, current_user.id == Ticket.customer_id))
    ticket = result.scalars().first()
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    await db.delete(ticket)
    await db.commit()

    return ticket


async def filter_ticket(db: AsyncSession, current_user: User, filters: Dict[str, str]) -> List[Ticket]:
    """
    Filters tickets based on provided filters.

    :param db:
    :param current_user:
    :param filters:
    :return:
    """

    query = select(Ticket).where(current_user.id == Ticket.customer_id)

    if filters: # Can be used ilike //Ticket.city.ilike(f"%{value}%")) elif key == 'hotel'// for finds all values containing the specified string anywhere
        for key, value in filters.items():
            if key == 'place':
                query = query.where(Ticket.place == value)
            elif key == 'city':
                query = query.where(Ticket.city == value)
            elif key == 'hotel':
                query = query.where(Ticket.hotel == value)
            elif key == 'latitude':
                query = query.where(Ticket.latitude == float(value))
            elif key == 'longitude':
                query = query.where(Ticket.longitude == float(value))

    result = await db.execute(query)
    return result.scalars().all()

async def get_coordinates(db: AsyncSession, current_user: User) -> List[Tuple[int, str, float, float]]:
    """
    :param db:
    :param current_user:
    :return:
    """

    result = await db.execute(
        select(Ticket.id, Ticket.hotel, Ticket.latitude, Ticket.longitude).where(current_user.id == Ticket.customer_id)
    )
    coordinates = result.mappings().all()
    print(coordinates)
    return coordinates