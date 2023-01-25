from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvredactionprofileDb(SchemaBase):
   __tablename__ = "iqvredactionprofile_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   DefaultIsRedacted = Column(INTEGER,nullable=False)

