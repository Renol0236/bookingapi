from fastapi import FastAPI
import asyncio
from fastapi.staticfiles import StaticFiles

from .api.endpoints import *
from .routers import auth, booking
from .db.base import Base, engine

app = FastAPI(title="BookingAPI")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#
#
# @app.on_event("startup")
# async def on_startup():
#     await init_db()


# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(booking.router, prefix="/booking", tags=["booking"])


@app.get('/')
async def root():
    return {"message": "BookingAPI"}
