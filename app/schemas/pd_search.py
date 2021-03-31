from typing import Optional

from pydantic import BaseModel


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


# Properties to receive via API on search
class SearchJson(SearchBase):
    key: str
    toc: list
    sponsor: list
    indication: list
    phase: list
    documentStatus: list
    dateType: str
    dateFrom: str
    dateTo: str

    sortField: str
    sortOrder: str
    pageNo: int
    pageSize: int
    qID: str
