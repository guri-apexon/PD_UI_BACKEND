from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvdocumentdiffDb(SchemaBase):
   __tablename__ = "iqvdocumentdiff_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   IsPreferredTermComparison = Column(BOOLEAN,nullable=False)
   confidence = Column(DOUBLE_PRECISION,nullable=False)
   local_roi_id = Column(TEXT)
   compare_roi_id = Column(TEXT)
   diff_type = Column(INTEGER,nullable=False)
   diff_string = Column(TEXT)
   diff_category = Column(TEXT)
   diff_subcategory = Column(TEXT)

