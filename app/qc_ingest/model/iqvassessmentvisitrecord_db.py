from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvassessmentvisitrecordDb(SchemaBase):
   __tablename__ = "iqvassessmentvisitrecord_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   doc_id = Column(TEXT)
   run_id = Column(TEXT)
   assessment = Column(TEXT)
   assessment_text = Column(TEXT)
   cycle_timepoint = Column(TEXT)
   day_timepoint = Column(TEXT)
   dts = Column(TEXT)
   epoch_timepoint = Column(TEXT)
   indicator_text = Column(TEXT)
   month_timepoint = Column(TEXT)
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
   visit_timepoint = Column(TEXT)
   week_timepoint = Column(TEXT)
   window_timepoint = Column(TEXT)
   year_timepoint = Column(TEXT)
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

Index('iqvassessmentvisitrecord_db_doc_id',IqvassessmentvisitrecordDb.doc_id)
