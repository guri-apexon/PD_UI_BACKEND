from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class LanguagecodeDb(SchemaBase):
   __tablename__ = "languagecode_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   code = Column(TEXT)
   description = Column(TEXT)
   tesseractCode = Column(TEXT)
   eTMFCode = Column(TEXT)
   fourLetterCode = Column(TEXT)
   ReleaseVersionAvailability = Column(INTEGER,nullable=False)

