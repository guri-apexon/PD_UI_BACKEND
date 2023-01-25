from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvcountrymappingDb(SchemaBase):
   __tablename__ = "iqvcountrymapping_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   Country = Column(TEXT)
   DateFormats_list = Column(TEXT)

