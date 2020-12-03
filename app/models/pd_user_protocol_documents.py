from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String

from app.db.base_class import Base


class PD_User_Protocol_Documents(Base):

    __tablename__ = "pd_user_protocol_documents"

    id = Column(Integer, primary_key=True, index=True)
    protocol_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    protocol_document_name = Column(String, nullable=True)
    protocol_document_status_id = Column(Integer, nullable=True)
    protocol_source_document_id = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_by = Column(String, nullable=True)
    #created_on = Column(datetime, nullable=False)
    modified_by = Column(String, nullable=True)
    #modified_on = Column(datetime, nullable=False)
