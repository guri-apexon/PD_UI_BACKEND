from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class PD_Protocol_Indication(Base):

    __tablename__ = "pd_protocol_indications"

    indId = Column(Integer, primary_key=True, index=True)
    indicationName = Column(String, nullable=True)
