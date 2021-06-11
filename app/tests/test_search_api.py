# import sys
# sys.path.append(r"C:\Users\q1061485\Desktop\Jupyter Notebooks\pd-section-extractor old\pd-ui-backend\17-May-2021\pd-ui-backend")

import pytest
from app import crud, schemas
from app.main import app
from fastapi.testclient import TestClient
from app.db.session import SessionLocal


client = TestClient(app)

return_fields = ["AiDocId", "ProtocolNo", "ProtocolTitle", "SponsorName", "Indication", "DocumentStatus", "phase",
                 "approval_date", "uploadDate", "MoleculeDevice", "is_active", "SourceFileName", "documentPath", "ProjectId",
                 "VersionNumber"
                 ]

key = "hcc"
toc = ["Protocol Summary" ,"Synopsis" , "Schema", "Schedule of Activities (SoA)", "Introduction", "Study Rationale",
       "Background", "Benefit/Risk Assessment", "Risk Assessment", "Benefit Assessment", "Overall Benefit: Risk Conclusion"]
sponsor = ["AstraZeneca", "Merck KGaA", "3D Medical", "NVT AG", "Eisai Co., Ltd."]
sponsor_astrazeneca = ["AstraZeneca"]
indication = ["ABCC6 deficiency"]
phase = ['II', 'I']
documentStatus = ["draft", "final"]
dateType_approval = "approval_date"
dateType_upload = "uploadDate"
dateFrom = "20130301"
dateTo = "20210304"
sortField_approval = "approval_date"
sortField_upload = "uploadDate"
sortOrder_asc = "asc"
sortOrder_desc = "desc"
pageNo = 1
pageSize = 100
qID = "q1061485"

toc_empty = []
key_empty = ""
sponsor_empty = []
indication_empty = []
phase_empty = []
documentStatus_empty = []
dateType_empty = ""
dateFrom_empty = ""
dateTo_empty = ""
sortField_empty = ""
sortOrder_empty = ""


@pytest.mark.parametrize(
    ["key", "toc", "sponsor", "indication", "phase", "documentStatus", "dateType", "dateFrom", "dateTo", "sortField", "sortOrder", "pageNo", "pageSize", "qID", "comment"],
    [(key, toc, sponsor, indication, phase, documentStatus, dateType_approval, dateFrom, dateTo, sortField_approval, sortOrder_asc, pageNo, pageSize, qID, "Check keyword and all filters."),
     (key, toc, sponsor, indication, phase_empty, documentStatus, dateType_empty, dateFrom, dateTo, sortField_approval, sortOrder_asc, pageNo, pageSize, qID, "Check keyword and empty phase and date type filters."),
     (key, toc, sponsor_empty, indication_empty, phase_empty, documentStatus_empty, dateType_empty, dateFrom_empty, dateTo_empty, sortField_empty, sortOrder_empty, pageNo, pageSize, qID, "Check keyword and all filters empty."),
     ("", toc_empty, sponsor, indication_empty, phase_empty, documentStatus_empty, dateType_empty, dateFrom_empty, dateTo_empty, sortField_empty, sortOrder_empty, pageNo, pageSize, qID, "Check sponsor filter."),
     ("", toc_empty, sponsor_empty, indication, phase_empty, documentStatus_empty, dateType_empty, dateFrom_empty, dateTo_empty, sortField_empty, sortOrder_empty, pageNo, pageSize, qID, "Check indication filter."),
     ("", toc_empty, sponsor_empty, indication_empty, phase, documentStatus_empty, dateType_empty, dateFrom_empty, dateTo_empty, sortField_empty, sortOrder_empty, pageNo, pageSize, qID, "Check phase filter."),
     ("", toc_empty, sponsor_empty, indication_empty, phase_empty, documentStatus, dateType_empty, dateFrom_empty, dateTo_empty, sortField_empty, sortOrder_empty, pageNo, pageSize, qID, "Check document status filter."),
     ("", toc_empty, sponsor_empty, indication_empty, phase_empty, documentStatus_empty, dateType_approval, dateFrom, dateTo, sortField_empty, sortOrder_empty, pageNo, pageSize, qID, "Check date range with approval date."),
     ("", toc_empty, sponsor_empty, indication_empty, phase_empty, documentStatus_empty, dateType_approval, dateTo, dateFrom, sortField_empty, sortOrder_empty, pageNo, pageSize, qID, "Check date range with approval date with incorrect date order."),
     ("", toc_empty, sponsor_empty, indication_empty, phase_empty, documentStatus_empty, dateType_upload, dateFrom, dateTo, sortField_empty, sortOrder_empty, pageNo, pageSize, qID, "Check date range with upload date."),
     ("", toc_empty, sponsor_empty, indication_empty, phase_empty, documentStatus_empty, dateType_upload, dateFrom, dateTo, sortField_empty, sortOrder_empty, pageNo, pageSize, qID, "Check date range with upload date with incorrect date order."),
     ("", toc_empty, sponsor_empty, indication_empty, phase_empty, documentStatus_empty, dateType_empty, dateFrom_empty, dateTo_empty, sortField_approval, sortOrder_asc, pageNo, pageSize, qID, "Check approval date sorting in ascending order."),
     ("", toc_empty, sponsor_empty, indication_empty, phase_empty, documentStatus_empty, dateType_empty, dateFrom_empty, dateTo_empty, sortField_approval, sortOrder_desc, pageNo, pageSize, qID, "Check approval date sorting in decending order."),
     ("", toc_empty, sponsor_empty, indication_empty, phase_empty, documentStatus_empty, dateType_empty, dateFrom_empty, dateTo_empty, sortField_upload, sortOrder_asc, pageNo, pageSize, qID, "Check upload date sorting in ascending order."),
     ("", toc_empty, sponsor_empty, indication_empty, phase_empty, documentStatus_empty, dateType_empty, dateFrom_empty, dateTo_empty, sortField_upload, sortOrder_desc, pageNo, pageSize, qID, "Check upload date sorting in decending order."),
     (key, toc, sponsor_astrazeneca, indication, phase, documentStatus, dateType_empty, dateFrom, dateTo, sortField_approval, sortOrder_asc, pageNo, pageSize, qID, "Ckeck with single sponsor."),
     (key, toc, sponsor_astrazeneca, indication, phase, documentStatus, dateType_empty, dateFrom, dateTo, sortField_approval, sortOrder_asc, 0, pageSize, qID, "Check for case where page no is 0/"),
     (key, toc, sponsor_astrazeneca, indication, phase, documentStatus, dateType_empty, dateFrom, dateTo, sortField_approval, sortOrder_asc, pageNo, 0, qID, "Check for case where page size is 0."),
     (key, toc, sponsor_astrazeneca, indication, phase, documentStatus, dateType_empty, dateFrom, dateTo, sortField_approval, sortOrder_asc, pageNo, pageSize, '', "Check for case where the QID is empty."),
     ])
def test_query_elastic(key, toc, sponsor, indication, phase, documentStatus, dateType, dateFrom, dateTo, sortField, sortOrder, pageNo, pageSize, qID, comment):

    search_json_in = schemas.SearchJson(key = key, toc = toc, sponsor = sponsor, indication = indication, phase = phase,
                                        documentStatus = documentStatus, dateType = dateType, dateFrom = dateFrom,
                                        dateTo = dateTo, sortField = sortField, sortOrder = sortOrder, pageNo = pageNo,
                                        pageSize = pageSize, qID = qID)

    db = SessionLocal()
    ret_fields = return_fields + toc if key else return_fields

    ret_val = crud.query_elastic(search_json_in, db, ret_fields)

    all_flags = list()

    if search_json_in.qID and search_json_in.pageNo and search_json_in.pageNo > 0 and search_json_in.pageSize and search_json_in.pageSize > 0:
        res_count = ret_val['count']
        res_count_flag = bool(res_count <= pageSize)
        all_flags.append(res_count_flag)

        if res_count:
            if key:
                key_flag = all([key in ' '.join(data.get(sec, '') for sec in toc).lower().split() for data in ret_val['data']])
                all_flags.append(key_flag)

            if sponsor:
                sponsor_flag = all([data['SponsorName'] in sponsor for data in ret_val['data']])
                all_flags.append(sponsor_flag)
                assert sponsor_flag

            if indication:
                indication_flag = all([data['Indication'] in indication for data in ret_val['data']])
                all_flags.append(indication_flag)
                assert indication_flag

            if phase:
                phase_flag = all([data['phase'] in phase for data in ret_val['data']])
                all_flags.append(phase_flag)
                assert phase_flag

            if documentStatus:
                documentStatus_flag = all([data['DocumentStatus'] in documentStatus for data in ret_val['data']])
                all_flags.append(documentStatus_flag)
                assert documentStatus_flag

            if dateType:
                dateType_flag = False
                if dateType == dateType_approval:
                    dateType_flag = all([data['approval_date'] >= dateFrom and data['approval_date'] <=  dateTo for data in ret_val['data']])
                elif dateType == dateType_upload:
                    dateType_flag = all([data['uploadDate'] >= dateFrom and data['uploadDate'] <=  dateTo for data in ret_val['data']])
                all_flags.append(dateType_flag)
                assert dateType_flag

            if sortField:
                sortField_flag = False
                if sortField == sortField_approval:
                    approval_dates = [data['approval_date'] for data in ret_val['data']]
                    length = len(approval_dates)
                    if sortOrder == sortOrder_asc:
                        if length > 1:
                            sortField_flag = all([approval_dates[idx] <= approval_dates[idx + 1] for idx in range(0, length - 1) if idx + 1 < length])
                        else:
                            sortField_flag = True
                    else:
                        if length > 1:
                            sortField_flag = all([approval_dates[idx] >= approval_dates[idx + 1] for idx in range(0, length - 1) if idx + 1 < length])
                        else:
                            sortField_flag = False

                elif sortField == sortField_upload:
                    upload_dates = [data['uploadDate'] for data in ret_val['data']]
                    length = len(upload_dates)
                    if sortOrder == sortOrder_asc:
                        if length > 1:
                            sortField_flag = all([upload_dates[idx] <= upload_dates[idx + 1] for idx in range(0, length - 1) if idx + 1 < length])
                        else:
                            sortField_flag = True
                    else:
                        if length > 1:
                            sortField_flag = all([upload_dates[idx] >= upload_dates[idx + 1] for idx in range(0, length - 1) if idx + 1 < length])
                        else:
                            sortField_flag = True

                all_flags.append(sortField_flag)
                assert(sortField_flag)

            if res_count == 0 and dateFrom > dateTo:
                all_flags.append(True)
                assert dateFrom > dateTo

        assert all(all_flags)
    else:
        assert 'data' not in ret_val




