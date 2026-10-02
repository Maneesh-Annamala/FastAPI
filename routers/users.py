# from contextlib import asynccontextmanager

# from fastapi.exception_handlers import http_exception_handler,request_validation_exception_handler
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter,HTTPException,status,Depends
from schemas import *
from models import *
from database import get_db
from sqlalchemy import select

from typing import Annotated

from auth import hash_password,verify_password,create_access_token,verify_access_token,oauth2_scheme,current_user
from datetime import timedelta
from sqlalchemy import func,select
from fastapi.security import OAuth2PasswordRequestForm
from core.config import settings



router = APIRouter(prefix="/api/users", tags=["Users"])

db_dependency = Annotated[AsyncSession, Depends(get_db)]


@router.post("",response_model=UserPrivate,status_code=status.HTTP_201_CREATED)
async def create_user(user : UserCreate, db : db_dependency):
    user_name = await db.execute(select(Users).where(func.lower(Users.username) == user.username.lower()))
    existing_user = user_name.scalars().first()
    user_email = await db.execute(select(Users).where(func.lower(Users.email) == user.email.lower()))
    existing_email = user_email.scalars().first()
    if existing_user or existing_email:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="User already exist")
    password = hash_password(user.password)
    new_user = Users(username=user.username,
                    email=user.email.lower(),
                    password=password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user,attribute_names=["posts"])
    return new_user

## login_for_access_token
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    # Look up user by email (case-insensitive)
    # Note: OAuth2PasswordRequestForm uses "username" field, but we treat it as email
    result = await db.execute(
        select(Users).where(
            func.lower(Users.email) == form_data.username.lower(),
        ),
    )
    user = result.scalars().first()

    # Verify user exists and password is correct
    # Don't reveal which one failed (security best practice)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token with user id as subject
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("", response_model=list[UserPublic])
async def get_users(db: db_dependency, current_user : current_user):
    result = await db.execute(select(Users).options(selectinload(Users.posts)))
    users = result.scalars().all()
    return users

@router.get("/current_user", response_model=UserPrivate)
async def get_current_user(current_user : current_user):
    return current_user

@router.get("/{user_id}/posts", response_model=list[PostResponse])
async def get_user_posts(user_id : int, db: db_dependency):
    result = await db.execute(select(Users).where(Users.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    result = await db.execute(select(Posts).options(selectinload(Posts.author))
                              .where(Posts.user_id == user.id)
                              .order_by(Posts.date_posted.desc())
                              )
    posts = result.scalars().all()
    return posts

@router.get("/{user_id}", response_model=UserPublic)
async def get_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Users).where(Users.id == user_id))
    user = result.scalars().first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.patch("/{user_id}", response_model=UserPrivate)
async def update_user(
    user_id : int,
    current_user : current_user,
    user_update: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)]):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Un-Authorized Action")
    if user_update.username is not None and user_update.username.lower() != current_user.username.lower():
        result = await db.execute(select(Users).where(func.lower(Users.username) == user_update.username.lower()))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already exists")
    if user_update.email is not None and user_update.email.lower() != users.email.lower():
        result = await db.execute(select(Users).where(func.lower(Users.email) == user_update.email.lower()))
        existing_email = result.scalars().first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
    if user_update.username is not None:
        current_user.username = user_update.username
    if user_update.email is not None:
        current_user.email = user_update.email.lower()
    if user_update.image_file is not None:
        current_user.image_file = user_update.image_file
    await db.commit()
    await db.refresh(current_user, attribute_names=["posts"])
    return current_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user : current_user, db: Annotated[AsyncSession, Depends(get_db)]):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Un-Authorized Action")
    # result = await db.execute(select(Users).where(Users.id == user_id))
    # user = result.scalars().first()
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="User not found",
    #     )
    await db.delete(current_user)
    await db.commit()

