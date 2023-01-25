from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvassessmentrecordDb(SchemaBase):
   __tablename__ = "iqvassessmentrecord_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   doc_id = Column(TEXT)
   run_id = Column(TEXT)
   assessment = Column(TEXT)
   assessment_text = Column(TEXT)
   num_visits = Column(INTEGER)
   dts = Column(TEXT)
   pname = Column(TEXT)
   procedure = Column(TEXT)
   procedure_text = Column(TEXT)
   ProcessMachineName = Column(TEXT)
   ProcessVersion = Column(TEXT)
   roi_id = Column(TEXT)
   section = Column(TEXT)
   table_link_text = Column(TEXT)
   DocumentSequenceIndex = Column(INTEGER,nullable=False)
   table_roi_id = Column(TEXT)
   table_sequence_index = Column(INTEGER)
   study_cohort = Column(TEXT)
   footnote_0 = Column(TEXT)
   footnote_1 = Column(TEXT)
   footnote_2 = Column(TEXT)
   footnote_3 = Column(TEXT)
   footnote_4 = Column(TEXT)
   footnote_5 = Column(TEXT)
   footnote_6 = Column(TEXT)
   footnote_7 = Column(TEXT)
   footnote_8 = Column(TEXT)
   footnote_9 = Column(TEXT)

Index('iqvassessmentrecord_db_doc_id',IqvassessmentrecordDb.doc_id)
