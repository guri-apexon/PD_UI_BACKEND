import os
from typing import Any, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

from starlette.responses import FileResponse
router = APIRouter()
PATH = '//INKOCWL000200/Users/q1036048/Desktop/__pycache__/PD/pd-management/'
#PATH = '//quintiles.net/enterprise/Services/protdigtest/pilot_iqvxml/'

@router.get("/", response_model=schemas.ProtocolMetadataDuplicateCheck)
def read_duplicate_attributes(
        db: Session = Depends(deps.get_db),
        sponsor: str = "sponsor",
        protocolNumber: str = "protocolNumber",
        versionNumber: str = "versionNumber",
        amendmentNumber: str = "amendmentNumber",
) -> Any:
    """
    Retrieve Duplicate Attributes.
    """
    duplicate_attributes = crud.pd_protocol_metadata.duplicate_check(db, sponsor, protocolNumber, versionNumber, amendmentNumber, documentStatus="final")
    return duplicate_attributes

@router.get("/shows/")
def get_items(q: List[str] = Query(None)):
    '''
    Pass path to function.
    Returns folders and files.
    '''

    results = {}

    query_items = {"q": q}
    if query_items["q"]:
        entry = PATH + "/".join(query_items["q"])
    else:
        entry = PATH

    print(os.path.isfile(entry))
    if os.path.isfile(entry):
        print("download start")
        return download(entry)

    dirs = os.listdir(entry + "/")
    results["folders"] = [
        val for val in dirs if os.path.isdir(entry + "/"+val)]
    results["files"] = [val for val in dirs if os.path.isfile(entry + "/"+val)]
    file_name = results["files"][-1]
    print(file_name)
    entry = entry + "/"+file_name
    print(entry)
    download(entry)
    results["path_vars"] = query_items["q"]

    return results

def download(file_path):
    """
    Download file for given path.
    """
    if os.path.isfile(file_path):
        print("downloaded")
        print(FileResponse(file_path))
        return FileResponse(path=file_path, media_type=".png", filename="docabhay.png")
        # return FileResponse(path=file_path)
    return None
