from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvredactioncategoryDb(SchemaBase):
   __tablename__ = "iqvredactioncategory_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   IsRedacted = Column(INTEGER,nullable=False)
   Category = Column(TEXT)
   Query = Column(TEXT)

