from datetime import timedelta

from app.schemas.pd_auth import Token
from app.utilities.auth import authenticate_user, create_access_token
from app.utilities.config import settings
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from jose import jwt, JWTError, ExpiredSignatureError

security = HTTPBasic()

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = settings.AUTH_ENDPOINT)


def raise_unauthorized_exception(detail = "Token validation failed"):
    raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = f"Credential validation: {detail}",
            headers = {"WWW-Authenticate": "Bearer"},
        )

def auth_create_token(username, password):
    """
    Authenticate credentials and create token
    """
    authorized_user = authenticate_user(settings.USERS_CRED, username, password)
    if not authorized_user:
        raise_unauthorized_exception(detail="Authentication failed for given username and password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": authorized_user}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

async def validate_user_token(token: str = Depends(oauth2_scheme)):
    """
    Validate the passed token
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        ref_string = payload.get("sub")
    except ExpiredSignatureError:
        raise_unauthorized_exception(detail = "Token is expired")
    except JWTError:
        raise_unauthorized_exception()

    ref_string_valid = ref_string in settings.USERS_CRED.keys()

    if not ref_string_valid:
        raise_unauthorized_exception(detail = "Invalid user")
    return True

@router.post("/", response_model=Token)
async def basic_authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Authenticate based on Basic Auth and create time-bound token
    """
    return auth_create_token(credentials.username, credentials.password)


@router.post("/form_data", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate based on form data's username/password and create time-bound token
    """
    return auth_create_token(form_data.username, form_data.password)
    