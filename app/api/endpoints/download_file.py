import os
import shutil
from typing import Any, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.utilities.config import settings
from starlette.responses import FileResponse
router = APIRouter()


@router.get("/")
def get_items(filePath: str = "filePath"):
    '''
    Pass path to function.
    Download files.
    '''

    try:
        status = download(filePath)
        if status is None:
            return "Downloading failed"
        else:
            fileName = filePath.split('\\')[-1]
            return fileName
    except FileNotFoundError as e:
        return "Folder does not exists"
        

def download(file_path):
    """
    Download file for given path.
    """
    if os.path.isfile(file_path):
        shutil.copy(file_path, settings.PROTOCOL_FOLDER)
        return FileResponse(path=file_path)
    return None
