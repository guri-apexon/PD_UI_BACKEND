from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.UserProtocol)
def follow_user_protocol(
        *,
        db: Session = Depends(deps.get_db),
        follow_protocol_in: schemas.UserFollowProtocol,
) -> Any:
    """
    push follow protocol data.
    """
    #user_protocol = crud.pd_user_protocols.create(db, obj_in=follow_protocol_in)
    user_protocol = crud.pd_user_protocols.follow_unfollow(db, obj_in=follow_protocol_in)
    return user_protocol


@router.delete("/", response_model=schemas.UserProtocol)
def delete_followed_protocols(
        *,
        db: Session = Depends(deps.get_db),
        id: str = "id",
        userId: str = "userId",
) -> Any:
    """
    Delete a saved search.
    """
    user_protocol = crud.pd_user_protocols.remove_followed_protocols(db, id, userId)
    return user_protocol


