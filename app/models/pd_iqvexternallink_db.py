from sqlalchemy import Column, DateTime, Integer, String, Boolean
from app.db.base_class import Base


class IqvexternallinkDb(Base):

    __tablename__ = "iqvexternallink_db"

    id = Column(String, primary_key=True)
    doc_id = Column(String , nullable=True)
    link_text = Column(String , nullable=True)
    link_id_subsection1 = Column(String , nullable=True)
    link_id_subsection2 = Column(String , nullable=True)
    link_id_subsection3 = Column(String , nullable=True)
    link_id = Column(String , nullable=True)
    link_id_level2 = Column(String , nullable=True)
    link_id_level3 = Column(String , nullable=True)
    link_id_level4 = Column(String , nullable=True)
    link_id_level5 = Column(String , nullable=True)
    link_id_level6 = Column(String , nullable=True)
    hierarchy = Column(String , nullable=True)
    startIndex = Column(Integer , nullable=True)
    connection_type = Column(String , nullable=True)
    destination_link_id = Column(String , nullable=True)
    source_text = Column(String , nullable=True)
    destination_url = Column(String , nullable=True)
    destination_link_prefix = Column(String , nullable=True)
    iqv_standard_term = Column(String , nullable=True)
    destination_link_text = Column(String , nullable=True)
    length = Column(Integer , nullable=True)
    group_type = Column(String , nullable=True)
    parent_id = Column(String , nullable=True)