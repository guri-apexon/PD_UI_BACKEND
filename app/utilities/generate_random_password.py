import random
import string
from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_random_alphanumeric_password(length: int = 40):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


generated_password = get_random_alphanumeric_password()

get_password_hash = generated_password