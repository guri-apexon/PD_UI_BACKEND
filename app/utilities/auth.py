from datetime import datetime, timedelta
from typing import Optional

from app.utilities.config import settings
from fastapi import APIRouter, FastAPI
from jose import jwt
from passlib.hash import pbkdf2_sha256

app = FastAPI()
router = APIRouter()

def verify_password(plain_password, hashed_password):
    """
    Verify the passed password with pre-computed hashed password
    """
    return pbkdf2_sha256.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Get password hash on the given password string based on specific # of rounds and salt size
    """
    return pbkdf2_sha256.using(rounds=8000, salt_size=10).hash(password)

def authenticate_user(users_db, username: str, password: str):
    """
    Authenticate the user/pwd
    """
    hashed_password = users_db.get(username, "")
    if not hashed_password:
        return False
    if not verify_password(password, hashed_password):
        return False
    return username

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create access token for the authenticated user session
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
