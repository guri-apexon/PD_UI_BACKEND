from typing import Any, List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from app.api.endpoints import auth
from app import crud
from app.utilities.extractor import cpt_extractor
import app.utilities.elastic_ingest as ei
from http import HTTPStatus

router = APIRouter()


@router.post("/")
async def elastic_ingest(
        aidoc_id: str,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    aidoc_id for saving document in Elastic Search
    """
    try:
        iqv_document, imagebinaries = crud.get_document_object(aidoc_id)
        if iqv_document:
            cpt_iqvdata = cpt_extractor.CPTExtractor(iqv_document,
                                                     imagebinaries,
                                                     dict(),
                                                     list())

            display_df, search_df, _, _, _ = cpt_iqvdata.get_cpt_iqvdata()
            db_data, summary_entities, es_save_doc_res = ei.ingest_doc_elastic(iqv_document,
                                                                               search_df,
                                                                               save_doc_elastic = True)

            msg = "Elastic ingest Completed Successfully" if es_save_doc_res else "Document could not be stored in Elastic search"
            return {"success": es_save_doc_res, "message":msg}
        else:
            return {"success": False, "message":"Document not found in DB."}

    except Exception as ex:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=f"Exception occurred while saving document in Elastic search: {str(ex)}")
