from typing import Generator

from app.db.session import SessionPSQL


def get_db() -> Generator:
    try:
        db = SessionPSQL()
        yield db
    finally:
        db.close()


# connection for postgresql
def get_psqldb() -> Generator:
    try:
        psdb = SessionPSQL()
        yield psdb
    finally:
        psdb.close()

