import uvicorn
from fastapi import APIRouter

from app.api.endpoints import indications
from app.api.endpoints import protocol_sponsor
from app.api.endpoints import protocols
from app.api.endpoints import protocol_metadata
from app.api.endpoints import recent_search
from app.api.endpoints import saved_search
from app.api.endpoints import document_status
from app.api.endpoints import duplicate_check
from app.api.endpoints import document_compare
from app.api.endpoints import related_protocols
from app.api.endpoints import protocol_data
from app.api.endpoints import protocol_qcdata
from app.api.endpoints import read_iqvdata
from app.api.endpoints import follow_protocol
from app.api.endpoints import download_file
from app.api.endpoints import mCRA
from app.api.endpoints import soft_delete
from app.api.endpoints import latest_approved_document
from app.api.endpoints import associated_docs
from app.api.endpoints import user_protocol
from app.api.endpoints import health_check
from app.api.endpoints import keyword_search
from app.api.endpoints import user_alert
from app.api.endpoints import notification_read
from app.api.endpoints import auth
from app.api.endpoints import pd_user_get_all_active_users
from app.api.endpoints import pd_user_UpdateExisting_SoftDelete
from app.api.endpoints import pd_user_login_CreateNewUser
from app.api.endpoints import pd_roles_GetAllRoles_CreateNewRoles
from app.api.endpoints import ldap_user_details
from app.api.endpoints import cpt_data
api_router = APIRouter()
api_router.include_router(health_check.router, prefix="/health", tags=["API Health Check"])
api_router.include_router(protocol_sponsor.router, prefix="/protocol_sponsor", tags=["Protocol Sponsors"])
api_router.include_router(indications.router, prefix="/indications", tags=["Indications"])
api_router.include_router(protocols.router, prefix="/protocols", tags=["Protocols"])
api_router.include_router(protocol_metadata.router, prefix="/protocol_metadata",
                          tags=["Protocol Metadata"])
api_router.include_router(document_compare.router, prefix="/document_compare", tags=["Compare Documents"])
api_router.include_router(protocol_data.router, prefix="/protocol_data", tags=["Protocol Data"])
api_router.include_router(protocol_qcdata.router, prefix="/protocol_qcdata", tags=["Protocol QC Data"])
api_router.include_router(read_iqvdata.router, prefix="/read_iqvdata", tags=["Read Iqvdata"])
api_router.include_router(recent_search.router, prefix="/recent_search", tags=["Recent Search"])
api_router.include_router(saved_search.router, prefix="/saved_search", tags=["Saved Search"])
api_router.include_router(document_status.router, prefix="/status", tags=["status"]) 
api_router.include_router(duplicate_check.router, prefix="/duplicate_check", tags=["Duplicate check"])
api_router.include_router(related_protocols.router, prefix="/Related_protocols", tags=["Related protocols"])
api_router.include_router(follow_protocol.router, prefix="/follow_protocol", tags=["Follow Protocol"])
api_router.include_router(download_file.router, prefix="/download_file", tags=["Download Files"])
api_router.include_router(mCRA.router, prefix="/latest_protocols", tags=["latest_protocols"])
api_router.include_router(soft_delete.router, prefix="/soft_delete", tags=["soft_delete"])
api_router.include_router(latest_approved_document.router, prefix="/latest_approved_document", tags=["Latest Approved Documents"])
api_router.include_router(associated_docs.router, prefix="/associated_docs", tags=["Associated Documents by protocols"])
api_router.include_router(user_protocol.router, prefix="/user_protocol", tags=["User Protocol"])

api_router.include_router(keyword_search.router, prefix="/keyword_search", tags=["Keyword Search"])
api_router.include_router(user_alert.router, prefix="/user_alert", tags=["User Alert"])
api_router.include_router(notification_read.router, prefix="/notification_read", tags=["User Alert Read Notification"])
api_router.include_router(auth.router, prefix="/token", tags=["Authentication"])
api_router.include_router(pd_user_get_all_active_users.router, prefix="/user", tags=["Retreving Active Users"])
api_router.include_router(pd_user_UpdateExisting_SoftDelete.router, prefix="/user_login", tags=["Update Existing Users & Soft Delete"])
api_router.include_router(pd_user_login_CreateNewUser.router, prefix="/create_new_user", tags=["Creating New User In User & Login"])
api_router.include_router(pd_roles_GetAllRoles_CreateNewRoles.router, prefix="/roles", tags=["Get All Roles And Create New Roles"])
api_router.include_router(ldap_user_details.router, prefix="/ldap_user_details", tags=["Retrieve User Details From LDAP"])
api_router.include_router(cpt_data.router, prefix="/cpt_data", tags=["Get CPT data for document"])