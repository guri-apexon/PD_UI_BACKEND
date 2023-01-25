from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvlanguagemappingDb(SchemaBase):
   __tablename__ = "iqvlanguagemapping_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   script_list = Column(TEXT)
   HistoricalCount = Column(INTEGER,nullable=False)
   HistoricalCountWeight = Column(DOUBLE_PRECISION,nullable=False)

