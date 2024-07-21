from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

from ..models.user import *
from ..schemas.user import UserCreate, Token
from ..core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from ..db.base import get_db

pdw_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    :param plain_password: The password to verify.
    :param hashed_password: The hashed password to compare against.
    :return: True if the passwords match, False otherwise.
    """
    return pdw_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str) -> str:
    """
    Hash a plain password.

    :param password: The password to hash.
    :return: The hashed password.
    """
    return pdw_context.hash(password)


async def get_user(db: AsyncSession, username: str) -> Optional[User]:
    """
    Retrieve a user by their username.

    :param db: The database session.
    :param username: The username of the user to retrieve.
    :return: The user if found, None otherwise.
    """
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()

async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
    """
    Authenticate a user by their username and password.

    :param db: The database session.
    :param username: The username of the user to authenticate.
    :param password: The password of the user to authenticate.
    :return: The user if authenticated, None otherwise.
    """
    user = await get_user(db, username)
    if not user or not await verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return user

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token.

    :param data: The data to encode into the access token.
    :param expires_delta: The time duration for which the access token should expire.
    :return: The encoded access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def register_user(db: AsyncSession, user_create: UserCreate) -> User:
    """
    Register a new user.

    :param db: The database session.
    :param user_create: The user data to create.
    :return: The newly created user.
    """
    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=await get_password_hash(user_create.password),
    )

    async with db.begin() as session:
        async_session = session.session
        async_session.add(user)
        await async_session.commit()

    return user

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """
    Retrieve the current user from the access token.

    :param db: The database session.
    :param token: The access token.
    :return: The current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user(db, username)
    if user is None:
        raise credentials_exception
    return user
