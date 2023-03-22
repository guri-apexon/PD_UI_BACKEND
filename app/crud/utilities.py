from typing import Any
from fastapi import Depends
from app import crud
from app.api import deps
from app.api.endpoints import auth
from sqlalchemy.orm import Session


async def get_preffered_data(
        db: Session = Depends(deps.get_db),
        doc_id: str = "",
        link_id: str = "",
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Get preffered terms values for the enriched text as per doc and section id
    :param db: database session
    :param doc_id: document id
    :param link_id: link id of document as section id
    :param _: To validate API token
    :returns: To collect all the preffered terms values for the enriched text
    from all over the section
    """
    config_variables = {"preferred_terms" : True}
    preffered_document_data = crud.get_document_terms_data(db, doc_id,
                                            link_id, config_variables, {})   
    
    preffered_data = []
    for entity in preffered_document_data[0].get("preferred_terms"):
        preffered_values = {
            'id': entity["id"],
            'parent_id': entity["parent_id"],
            'preferred_term': entity["preferred_term"],
            'text': entity["text"] 
        }
        preffered_data.append(preffered_values)

    return preffered_data
