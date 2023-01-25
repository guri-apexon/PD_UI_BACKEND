from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvdocumentvariableDb(SchemaBase):
   __tablename__ = "iqvdocumentvariable_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   doc_id = Column(TEXT)
   dts = Column(TEXT)
   run_id = Column(TEXT)
   variable_key = Column(TEXT)
   variable_value = Column(TEXT)
   variable_datatype = Column(TEXT)
   variable_notes = Column(TEXT)
   variable_score = Column(DOUBLE_PRECISION,nullable=False)
   variable_source = Column(TEXT)
   variable_listing_filename = Column(TEXT)
   source_filename = Column(TEXT)
   variable_label = Column(TEXT)
   variable_category = Column(TEXT)
   variable_index = Column(INTEGER,nullable=False)

