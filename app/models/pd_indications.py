from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class PD_Protocol_Indication(Base):

    __tablename__ = "pd_protocol_indications"

    id = Column(Integer, primary_key=True, index=True)
    indication_name = Column(String, nullable=True)
    indication_description = Column(String, nullable=True)
