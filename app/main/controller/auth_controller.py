import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.main.database import get_db
from app.main.schemas.Schemas import Token, User, UserInDB, UserIn
import app.main.services.auth_service as auth_service

router = APIRouter(prefix="/auth",
                   tags=["auth"])


@router.post("/token",
             response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logging.info("login_for_access_token")
    user = auth_service.authenticate_user(db,
                                          form_data.username,
                                          form_data.password)
    if not user:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(data={"sub": user.username},
                                                    expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model= User)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user

@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(auth_service.get_current_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

@router.post("/register")
async def register_user(user: UserIn, db: Session = Depends(get_db)):
    return auth_service.register_user(db,
                                      user)
