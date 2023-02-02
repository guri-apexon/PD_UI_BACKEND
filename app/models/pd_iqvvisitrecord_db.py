from sqlalchemy import Column, DateTime, Integer, String, Boolean
import datetime
from app.db.base_class import Base


class IqvvisitrecordDb(Base):

    __tablename__ = "iqvvisitrecord_db"
    
    id = Column(String, primary_key=True)
    doc_id = Column(String , nullable=True)
    day_timepoint = Column(String , nullable=True)
    window_timepoint  = Column(String , nullable=True)
    cycle_timepoint = Column(String , nullable=True)
    table_roi_id = Column(String , nullable=True)
    visit_timepoint = Column(String , nullable=True)
    epoch_timepoint = Column(String , nullable=True)
    table_link_text = Column(String , nullable=True)
    num_assessments = Column(Integer , nullable=True)
    DocumentSequenceIndex = Column(Integer , nullable=True)
    year_timepoint = Column(String , nullable=True)
    ProcessMachineName = Column(String , nullable=True)
    pname = Column(String , nullable=True)
    month_timepoint = Column(String , nullable=True)
    study_cohort = Column(String , nullable=True)
    week_timepoint = Column(String , nullable=True)
    footnote_0 = Column(String , nullable=True)
    ProcessVersion = Column(String , nullable=True)
    table_sequence_index = Column(Integer , nullable=True)
    footnote_1 = Column(String , nullable=True)
    footnote_2 = Column(String , nullable=True)
    footnote_3 = Column(String , nullable=True)
    footnote_4 = Column(String , nullable=True)
    footnote_5 = Column(String , nullable=True)
    footnote_6 = Column(String , nullable=True)
    footnote_7 = Column(String , nullable=True)
    footnote_8 = Column(String , nullable=True)
    footnote_9 = Column(String , nullable=True)
    run_id = Column(String , nullable=True)
    indicator_text = Column(String , nullable=True)
    dts = Column(String , nullable=True)

    