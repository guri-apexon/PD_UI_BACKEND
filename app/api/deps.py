from typing import Generator

from app.db.session import SessionPSQL


def get_db() -> Generator:
    try:
        db = SessionPSQL()
        yield db
    finally:
        db.close()
