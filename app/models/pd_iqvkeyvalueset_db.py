from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class IqvkeyvaluesetDb(Base):

    __tablename__ = "iqvkeyvalueset_db"

    id = Column(String, primary_key=True)
    doc_id = Column(String , nullable=True)
    rawScore = Column(Integer , nullable=True)
    source_system = Column(String , nullable=True)
    link_id = Column(String , nullable=True)
    link_id_level2 = Column(String , nullable=True)
    link_id_level3 = Column(String , nullable=True)
    link_id_level4 = Column(String , nullable=True)
    link_id_level5 = Column(String , nullable=True)
    link_id_level6 = Column(String , nullable=True)
    confidence = Column(Integer , nullable=True)
    hierarchy = Column(String , nullable=True)
    parent_id = Column(String , nullable=True)
    group_type = Column(String , nullable=True)
    link_id_subsection1 = Column(String , nullable=True)
    link_id_subsection2 = Column(String , nullable=True)
    link_id_subsection3 = Column(String , nullable=True)
    value = Column(String , nullable=True)
    key = Column(String , nullable=True)
    iqv_standard_term = Column(String , nullable=True)