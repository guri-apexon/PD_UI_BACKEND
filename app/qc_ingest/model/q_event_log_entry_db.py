from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class QEventLogEntryDb(SchemaBase):
   __tablename__ = "q_event_log_entry_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   bHandled = Column(BOOLEAN,nullable=False)
   m_DateTimeStampVal = Column(TEXT)
   UserID = Column(TEXT)
   UserEmail = Column(TEXT)
   UserInputMessage = Column(TEXT)
   ErrorLevelVal = Column(INTEGER,nullable=False)
   EventTypeVal = Column(INTEGER,nullable=False)
   Message = Column(TEXT)
   StackTrace = Column(TEXT)
   ClassMapping = Column(TEXT)
   FieldMapping = Column(TEXT)
   Value = Column(TEXT)
   DocumentID = Column(TEXT)
   DocumentName = Column(TEXT)
   DocumentPage = Column(INTEGER,nullable=False)
   CountReplace = Column(INTEGER,nullable=False)

