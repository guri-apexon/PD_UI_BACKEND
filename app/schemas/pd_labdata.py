from typing import Optional, List

from pydantic import BaseModel


# Shared properties
class LabDataBase(BaseModel):
    id : Optional[str] = None
    doc_id : Optional[str] = None
    run_id : Optional[str] = None
    parameter : Optional[str] = None
    parameter_text : Optional[str] = None
    procedure_panel : Optional[str] = None
    procedure_panel_text : Optional[str] = None
    assessment : Optional[str] = None
    dts : Optional[str] = None
    pname : Optional[str] = None
    ProcessMachineName : Optional[str] = None
    ProcessVersion : Optional[str] = None
    roi_id : Optional[str] = None
    section : Optional[str] = None
    table_link_text : Optional[str] = None
    table_roi_id : Optional[str] = None
    table_sequence_index : Optional[str] = None
    request_type: Optional[str] = None


class LabDataCreate(BaseModel):
    data: LabDataBase


class LabDataUpdate(BaseModel):
    data: List[LabDataBase]


class LabDataDelete(BaseModel):
    doc_id: Optional[str] = None
    roi_id: Optional[str] = None
    table_roi_id: Optional[str] = None


class LabData(BaseModel):
    data: LabDataDelete
