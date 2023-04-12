from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()


@router.post("/", response_model=schemas.UserProtocol)
def follow_user_protocol(
        *,
        db: Session = Depends(deps.get_db),
        _: str = Depends(auth.validate_user_token),
        follow_protocol_in: schemas.UserFollowProtocol,
) -> Any:
    """
    push follow protocol data.
    """
    user_protocol = crud.pd_user_protocols.follow_unfollow(db, obj_in=follow_protocol_in)
    # To update user global setting based on protocol follow/unfollow
    crud.user.follow_protocol_to_update_user_setting(db=db,
                                                     user_id=follow_protocol_in.userId,
                                                     follow=follow_protocol_in.follow)
    return user_protocol


@router.delete("/", response_model=schemas.UserProtocol)
def delete_followed_protocols(
        *,
        db: Session = Depends(deps.get_db),
        _: str = Depends(auth.validate_user_token),        
        id: str = "id",
        userId: str = "userId",
) -> Any:
    """
    Delete a saved search.
    """
    user_protocol = crud.pd_user_protocols.remove_followed_protocols(db, id, userId)
    return user_protocol


