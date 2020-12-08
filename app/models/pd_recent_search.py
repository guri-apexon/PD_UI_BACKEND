from sqlalchemy import Column, DateTime, Integer, String
from datetime import datetime
from app.db.base_class import Base


class PD_Protocol_Recent_Search(Base):

    __tablename__ = "pd_protocol_recent_search"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, nullable=True)
    user = Column(String, nullable=True)
    timeCreated = Column(DateTime(timezone=True), default=datetime.utcnow)
    lastUpdated = Column(DateTime(timezone=True), default=datetime.utcnow)
