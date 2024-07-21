from fastapi import APIRouter, Depends, HTTPException, status, Query
from starlette.responses import HTMLResponse, JSONResponse

from ..db.base import get_db
from ..schemas.booking import TicketCreate, TicketOut, TicketUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import get_current_user
from app.services import booking_service
from ..models.user import *
from ..models import user
from typing import List
import folium

router = APIRouter()


@router.post('/', response_model=TicketOut, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_db),
                        current_user: user.User = Depends(get_current_user
                                                          )):
    """
    Create a new ticket.

    :param ticket:
    :param db:
    :param current_user:
    :return:
    """
    return await booking_service.create_ticket(ticket, db, current_user)


@router.get('/', response_model=List[TicketOut])
async def get_all_tickets(db: AsyncSession = Depends(get_db),
                          current_user: user.User = Depends(get_current_user)):
    """
    Get all tickets.

    :param db:
    :param current_user:
    :return:
    """
    return await booking_service.get_all_tickets(db, current_user)


@router.get('/{ticket_id}', response_model=TicketOut)
async def get_ticket(
        ticket_id: int,
        db: AsyncSession = Depends(get_db),
        current_user:
        user.User = Depends(get_current_user)
):
    """
    Get a ticket by ID.

    :param ticket_id: 
    :param db:
    :param current_user:
    :return:
    """
    return await booking_service.get_ticket(ticket_id, db, current_user)


@router.put("/{ticket_id}", response_model=TicketOut)
async def update_ticket(ticket_id: int, ticket_update: TicketUpdate,
                        db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    """
    Update a ticket by ID.

    :param ticket_id:
    :param ticket_update:
    :param db:
    :param current_user:
    :return:
    """
    return await booking_service.update_ticket(ticket_id=ticket_id,
                                               ticket_update=ticket_update,
                                               db=db,
                                               current_user=current_user)


@router.delete("/{ticket_id}", response_model=TicketOut)
async def delete_ticket(
        ticket_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await booking_service.delete_ticket(ticket_id, db, current_user)


@router.get("/filter/filter", response_model=List[TicketOut])
async def get_filtered_tickets(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
        place: str = Query(None),
        city: str = Query(None),
        hotel: str = Query(None),
        latitude: float = Query(None),
        longitude: float = Query(None),
):
    """
    Get filtered tickets.

    :param db:
    :param current_user:
    :param place:
    :param city:
    :param hotel:
    :param latitude:
    :param longitude:
    :return:
    """
    filters = {
        "place": place,
        "city": city,
        "hotel": hotel,
        "latitude": latitude,
        "longitude": longitude,
    }

    filters = {key: value for key, value in filters.items() if value is not None}

    tickets = await booking_service.filter_ticket(db, current_user, filters)

    if tickets is None:
        return []

    return tickets


@router.get('/visualize/map')
async def visualize_map(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = await booking_service.get_coordinates(db, current_user)

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tickets found for the user.")

    first_entry = data[0]
    m = folium.Map(location=[first_entry['latitude'], first_entry['longitude']], zoom_start=12)
    for entry in data:
        lat = entry['latitude']
        lon = entry['longitude']
        ticket_id = entry['id']
        hotel = entry['hotel']

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='red',
            fill=True,
            fill_color='red',
            popup=f"ID: {ticket_id}, Hotel: {hotel}"
        ).add_to(m)

    map_html = m._repr_html_()

    return HTMLResponse(content=map_html)
