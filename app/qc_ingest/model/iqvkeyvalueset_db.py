from sqlalchemy import Column
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, TEXT, VARCHAR


class IqvkeyvaluesetDb(SchemaBase):
    __tablename__ = "iqvkeyvalueset_db"
    id = Column(VARCHAR(128), primary_key=True, nullable=False)
    doc_id = Column(TEXT)
    link_id = Column(TEXT)
    link_id_level2 = Column(TEXT)
    link_id_level3 = Column(TEXT)
    link_id_level4 = Column(TEXT)
    link_id_level5 = Column(TEXT)
    link_id_level6 = Column(TEXT)
    link_id_subsection1 = Column(TEXT)
    link_id_subsection2 = Column(TEXT)
    link_id_subsection3 = Column(TEXT)
    hierarchy = Column(VARCHAR(128), primary_key=True, nullable=False)
    iqv_standard_term = Column(TEXT)
    parent_id = Column(TEXT)
    group_type = Column(TEXT)
    source_system = Column(TEXT)
    key = Column(TEXT)
    value = Column(TEXT)
    confidence = Column(DOUBLE_PRECISION, nullable=False)
    rawScore = Column(DOUBLE_PRECISION, nullable=False)
