from sqlalchemy import ARRAY,Column, DateTime, Integer, String, Boolean
from enum import Enum
from datetime import datetime
from app.db.base_class import Base
class PD_WorkFlowState(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PAUSE = "PAUSE"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


class PD_WorkFlow_Status(Base):
    __tablename__ = 'work_flow_status'
    work_flow_id = Column(String, primary_key=True)
    doc_id= Column(String)
    protocol_name = Column(String, nullable=False)
    doc_uid = Column(String)
    work_flow_name = Column(String)
    documentFilePath = Column(String(500))
    status = Column(
        String, default=PD_WorkFlowState.PENDING.value)
    all_services = Column(ARRAY(String), default=[])
    running_services = Column(
        ARRAY(String), default=[])  # name of service
    finished_services = Column(ARRAY(String), default=[])
    percent_complete = Column(Integer(), default=0)
    lastUpdated = Column(DateTime(timezone=True), default=datetime.utcnow,
                                    onupdate=datetime.utcnow)
    timeCreated = Column(DateTime(
        timezone=True), default=datetime.utcnow)
    isProcessing = Column(Boolean, default=True)
    errorCode = Column(Integer(), default=0)
    errorReason = Column(String, default='')
    errorMessageDetails = Column(String, default='')
