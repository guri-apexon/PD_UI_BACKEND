from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvdocumentmappingDb(SchemaBase):
   __tablename__ = "iqvdocumentmapping_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   Document_Description = Column(TEXT)
   DOC_CLASS = Column(TEXT)
   DOC_ZONE = Column(TEXT)
   DOC_SECTION = Column(TEXT)
   DOC_ARTIFACT = Column(TEXT)
   DOC_ABBREVIATION = Column(TEXT)
   DIA_KEY = Column(TEXT)
   CONTENT_TYPE = Column(TEXT)
   DOC_COUNT = Column(INTEGER,nullable=False)
   DOC_COUNT_CURRENT = Column(INTEGER,nullable=False)
   Wingspan_Doc_ID = Column(TEXT)
   Wingspan_DIA = Column(TEXT)
   Wingspan_doc_type = Column(TEXT)
   Subtype = Column(TEXT)
   Subject = Column(TEXT)
   DateGuidance = Column(TEXT)
   DateGuidanceSecondary = Column(TEXT)
   TargetSystemName = Column(TEXT)
   TargetSystemVersion = Column(TEXT)
   ExpirationDateExpected = Column(INTEGER,nullable=False)
   Additional_instructions = Column(TEXT)
   Full_Classification_Wingspan = Column(TEXT)
   Full_Classification_Historical = Column(TEXT)
   MLConfusionCluster = Column(TEXT)
   MLClassificationGroup = Column(TEXT)
   MLClassificationRole = Column(TEXT)

