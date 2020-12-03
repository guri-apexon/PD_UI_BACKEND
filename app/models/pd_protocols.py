from sqlalchemy import Boolean, Column, Integer, String
from datetime import datetime

from app.db.base_class import Base


class PD_Protocols(Base):

    __tablename__ = "pd_protocols"

    id = Column(Integer, primary_key=True, index=True)
    protocol_number = Column(String, nullable=True)
    protocol_title = Column(String, nullable=True)
    project_code = Column(String, nullable=True)
    phase = Column(Integer, nullable=True)
    indication = Column(String, nullable=True)
    protocol_status = Column(Integer, nullable=True)
    protocol_version = Column(String, nullable=True)
    protocol_sponsor = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_by = Column(String, nullable=True)
    #created_on = Column(datetime, nullable=False)
    modified_by = Column(String, nullable=True)
    #modified_on = Column(datetime, nullable=False)
