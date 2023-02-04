from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class PD_Protocol_Sponsor(Base):

    __tablename__ = "PD_Protocol_Sponsor"

    sponsorId = Column(Integer, primary_key=True, index=True)
    sponsorName = Column(String, nullable=True)
