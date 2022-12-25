from datetime import timedelta, datetime

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.main.database import get_db
from app.main.model import models
from app.main.model.models import User
from app.main.schemas.Schemas import TokenData, UserIn

SECRET_KEY = '1bed178d1bc439a956c903ef3c0086318834e860e00cd20ab64b62bcbdeb2649'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,
                              hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def register_user(db: Session, user: UserIn):
    if get_user(db,
                username=user.username):
        raise HTTPException(status_code=400,
                            detail="User already exists")

    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password,
                          is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db, username: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user




def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db,
                    username)
    if not verify_password(password,
                           user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             SECRET_KEY,
                             algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token,
                             SECRET_KEY,
                             algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(db,
                    username=token_data.username)

    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400,
                            detail="Inactive user")
    return current_user


