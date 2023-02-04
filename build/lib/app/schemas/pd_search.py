from typing import Optional, List

from pydantic import BaseModel, Field


# Shared properties
class SearchBase(BaseModel):
    key: Optional[str] = None
    toc: Optional[list] = None  # ["Protocol Summary", "Introduction"]
    sponsor: Optional[list] = None  # ["Abbott Devices", "Abbott Egypt"]
    indication: Optional[list] = None  # ["ABCC6 deficiency", "Acne"]
    phase: Optional[list] = None  # ["Phase 0", "Phase 1b"]
    documentStatus: Optional[list] = None  # ["draft", "final"]
    dateType: Optional[str] = None  # "uploadDate"
    dateFrom: Optional[str] = None  # "20210301"
    dateTo: Optional[str] = None  # "20210304"
    sortField: Optional[str] = None  # uploadDate, approval_date, relevancy
    sortOrder: Optional[str] = None  # asc, desc
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    qID: Optional[str] = None
    qcStatus: Optional[List[str]] = None


# Properties to receive via API on search
class SearchJson(SearchBase):
    pageNo: int = Field(..., gt=0)
    pageSize: int = Field(..., gt=0)
    qID: str = Field(..., min_length=1)
    dateType: str = Field(None, regex='^uploadDate|approval_date|$')
    qcStatus: List[str] = Field(None, regex='^QC_NOT_STARTED|QC1|QC2|QC_COMPLETED$', max_items=4)