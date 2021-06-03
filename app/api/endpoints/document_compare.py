from typing import Any, List

from fastapi import APIRouter, Depends
from app.crud.pd_document_compare import pd_document_compare
from sqlalchemy.orm import Session
import os
from app import crud, schemas
from app.api import deps
import shutil
from fastapi import HTTPException
from app.utilities.config import settings

router = APIRouter()

@router.get("/", response_model=schemas.DocumentCompare)
def get_compare_doc(
        db: Session = Depends(deps.get_db),
        id1: str = "id",
        id2: str = "id2"
) -> Any:
    """
    Get the compare file path and number of changes.
    """
    document_process = pd_document_compare.get_compare_path(db, id1, id2)
    if document_process is None:
        raise HTTPException(status_code=404, detail=f"No record found for the given IDs")
    else:
        try:
            if document_process:
                    compare_path = document_process.compareCSVPath
                    new_path = settings.PROCESSING_DIR
                    transfer_path = '/'.join(new_path.split('/')[:-1])
                    shutil.copy(compare_path, os.path.join(transfer_path,'compare_csv'))
            else:
                    None
        except Exception as ex:
            raise HTTPException(status_code=404, detail=f"No data found for the give id's")
    return document_process
