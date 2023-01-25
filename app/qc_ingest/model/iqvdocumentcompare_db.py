from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvdocumentcompareDb(SchemaBase):
   __tablename__ = "iqvdocumentcompare_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   redaction_profile_id = Column(TEXT)
   compare_doc_id = Column(TEXT)
   compare_doc_name = Column(TEXT)
   base_doc_id = Column(TEXT)
   base_doc_name = Column(TEXT)

