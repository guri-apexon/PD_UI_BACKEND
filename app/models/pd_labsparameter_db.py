from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base


class IqvlabparameterrecordDb(Base):
    __tablename__ = "iqvlabparameterrecord_db"

    id = Column(String, primary_key=True)
    doc_id = Column(String, nullable=True)
    run_id = Column(String, nullable=True)
    parameter = Column(String, nullable=True)
    parameter_text = Column(String, nullable=True)
    procedure_panel = Column(String, nullable=True)
    procedure_panel_text = Column(String, nullable=True)
    assessment = Column(String, nullable=True)
    dts = Column(String, nullable=True)
    pname = Column(String, nullable=True)
    ProcessMachineName = Column(String, nullable=True)
    ProcessVersion = Column(String, nullable=True)
    roi_id = Column(String, nullable=True)
    section = Column(String, nullable=True)
    table_link_text = Column(String, nullable=True)
    table_roi_id = Column(String, nullable=True)
    table_sequence_index = Column(Integer, nullable=True)
    soft_delete = Column(Boolean, nullable=True)
