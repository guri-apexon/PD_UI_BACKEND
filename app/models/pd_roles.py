from sqlalchemy import Column, String, Integer
from app.db.base_class import Base

class Roles(Base):
    __tablename__ = "pd_roles"
    id = Column(Integer, primary_key=True, index=True)
    roleName = Column(String, nullable=True)
    roleDescription = Column(String, nullable=True)