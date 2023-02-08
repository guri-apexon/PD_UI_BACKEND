from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class IqvdocumentlinkDb(Base):

    __tablename__ = "iqvdocumentlink_db"


    id = Column(String, primary_key=True)
    link_id = Column(String , nullable=True)
    link_id_level2 = Column(String , nullable=True)
    link_id_level3 = Column(String , nullable=True)
    link_id_level4 = Column(String , nullable=True)
    link_id_level5 = Column(String , nullable=True)
    link_id_level6 = Column(String , nullable=True)
    link_id_subsection1 = Column(String , nullable=True)
    link_id_subsection2 = Column(String , nullable=True)
    link_id_subsection3 = Column(String , nullable=True)
    LinkType = Column(String , nullable=True)
    iqv_standard_term = Column(String , nullable=True)
    doc_id = Column(String , nullable=True)
    LinkLevel = Column(Integer , nullable=True)
    LinkPrefix = Column(String , nullable=True)
    LinkPage = Column(Integer , nullable=True)
    parent_id = Column(String , nullable=True)
    LinkText = Column(String , nullable=True)
    group_type = Column(String , nullable=True)
    hierarchy = Column(String , nullable=True)
    DocumentSequenceIndex = Column(Integer , nullable=True)