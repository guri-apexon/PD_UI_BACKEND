from sqlalchemy import Column, Integer, String, TIMESTAMP

from app.db.base_class import Base


class PdEmailTemplates(Base):

    __tablename__ = "pd_email_templates"

    id = Column(Integer, primary_key=True, index=True)
    event = Column(String, nullable=True)
    email_body = Column(String, nullable=True)
    create_time = Column(TIMESTAMP, nullable=True)
    updated_time = Column(TIMESTAMP, nullable=True)
    subject = Column(String, nullable=True)