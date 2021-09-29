from sqlalchemy import Column, DateTime, Integer, String, VARCHAR, Boolean
from datetime import datetime
from app.db.base_class import Base


class PD_Document_Compare(Base):

    __tablename__ = "pd_protocol_compare"


    compareId = Column(String, primary_key=True)
    id1 = Column(String)
    id2 = Column(String)
    protocolNumber = Column(String(45))
    compareIqvXmlPath = Column(String(1000))
    compareCSVPath = Column(String(1000))
    compareJSONPath =Column(String(1000))
    compareCSVPathNormSOA = Column(String(1000))
    compareJSONPathNormSOA = Column(String(1000))
    redactProfile = Column(String(100))
    feedbackRun = Column(Integer())
    compareExcelPathNormSOA = Column(String(1000))
    compareHTMLPathNormSOA = Column(String(1000))
    numChangesTotal = Column(Integer())
    swap = Column(Boolean(), default=False)
    createdDate = Column(DateTime)
    updatedDate = Column(DateTime)
