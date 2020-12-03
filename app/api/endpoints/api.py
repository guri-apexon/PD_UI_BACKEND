from fastapi import APIRouter

from app.api.endpoints import indications
from app.api.endpoints import protocol_sponsor
from app.api.endpoints import protocols
from app.api.endpoints import user_protocol_documents

api_router = APIRouter()
api_router.include_router(protocol_sponsor.router, prefix="/protocol_sponsor", tags=["Protocol Sponsors"])
api_router.include_router(indications.router, prefix="/indications", tags=["Indications"])
api_router.include_router(protocols.router, prefix="/protocols", tags=["Protocols"])
api_router.include_router(user_protocol_documents.router, prefix="/user_protocol_documents",
                          tags=["User Protocol Documents"])
