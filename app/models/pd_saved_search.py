from sqlalchemy import Column, DateTime, Integer, String
from datetime import datetime
from app.db.base_class import Base


class PD_Protocol_Saved_Search(Base):

    __tablename__ = "pd_protocol_saved_search"

    saveId = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, nullable=True)
    userId = Column(String, nullable=True)
    timeCreated = Column(DateTime(timezone=True), default=datetime.utcnow)
    lastUpdated = Column(DateTime(timezone=True), default=datetime.utcnow)