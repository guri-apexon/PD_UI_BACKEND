from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class PD_Protocol_Sponsor(Base):

    __tablename__ = "PD_Protocol_Sponsor"

    id = Column(Integer, primary_key=True, index=True)
    sponsor_name = Column(String, nullable=True)
    sponsor_abbreviation = Column(String, nullable=True)
