import concurrent.futures
import logging
from http import HTTPStatus

import pandas as pd
from app import config, schemas
from app.models.pd_user_protocols import PD_User_Protocols
from app.utilities.config import settings
from app.utilities.elastic_utilities import search_elastic
from app.utilities.redact import redactor
from .pd_user import user


logger = logging.getLogger(settings.LOGGER_NAME)

return_fields = ["AiDocId", "ProtocolNo", "ProtocolTitle", "SponsorName", "Indication", "DocumentStatus", "phase",
                 "approval_date", "uploadDate", "UserId", "MoleculeDevice", "is_active", "SourceFileName",
                 "documentPath", "ProjectId", "VersionNumber", "qcStatus"
                 ]


def create_keyword_query(search_json_in: schemas.SearchJson, apply_toc_filter = False):
    """
        Query json for keyword i.e. text entered by user in search bar is created and returned.
    """
    try:
        if search_json_in.key is None or search_json_in.key == '':
            return False
        keyword_query = dict()
        keyword_query['multi_match'] = dict()
        keyword_query['multi_match']['query'] = search_json_in.key
        keyword_query['multi_match']['type'] = "phrase"  # Need to change this on the basis of "" for phrase
        if apply_toc_filter and search_json_in.toc:
            keyword_query['multi_match']['fields'] = search_json_in.toc
        return keyword_query
    except Exception as e:
        logger.exception("Exception Inside create_keyword_query function: {}".format(e))
        return False


def create_keyword_filter_query(keyword_list, field):
    """
    Query json for filter field selected by user is created and returned.
    """
    try:
        if keyword_list:
            query = {'terms': {field + '.keyword': keyword_list}}
        else:
            query = False
    except Exception as e:
        logger.exception("Exception Inside create_keyword_filter: {}".format(e))
        query = False
    return query


def create_date_range_query(dateFrom, dateTo, dateType):
    """
    Creates json for date range query. dateType is uploadDate and length of the date is 8, 000000 is added at end of dateFrom
    and 235959 is to end of dateTo. Else the date values received in the request is used in the query without modification.
    """
    try:
        date_type_values = ["uploadDate", "approval_date"]
        if dateType == "uploadDate" and len(dateFrom) == 8:
            dateFrom = dateFrom + "000000"
        if dateType == "uploadDate" and len(dateTo) == 8:
            dateTo = dateTo + "235959"
        if dateFrom != "" and dateTo != "" and dateType in date_type_values:
            query = {'range': {dateType: {"gte": dateFrom, "lte": dateTo}}}
        else:
            query = False
    except Exception as e:
        logger.exception("Exception Inside create_date_range_query: {}".format(e))
        query = False
    return query


def create_filter_query(search_json_in: schemas.SearchJson):
    """
    Query json for filters selected by user is created and returned. Filter values that can be selected by user are for
    1. Indication
    2. Sponsor
    3. Phase
    4. Document Status
    5. Date range
    """
    try:
        filter_query = list()
        # Indication filter
        query = create_keyword_filter_query(search_json_in.indication, "Indication")
        if query:
            filter_query.append(query)
        # Sponsor filter
        query = create_keyword_filter_query(search_json_in.sponsor, "SponsorName")
        if query:
            filter_query.append(query)
        # Phase filter
        query = create_keyword_filter_query(search_json_in.phase, "phase")
        if query:
            filter_query.append(query)
        # Document status filter
        query = create_keyword_filter_query(search_json_in.documentStatus, "DocumentStatus")
        if query:
            filter_query.append(query)
        # qcStatus filter
        query = create_keyword_filter_query(search_json_in.qcStatus, "qcStatus")
        if query:
            filter_query.append(query)

        # Date range filter
        query = create_date_range_query(search_json_in.dateFrom, search_json_in.dateTo, search_json_in.dateType)
        if query:
            filter_query.append(query)
        filter_query = {"bool": {"must": filter_query}}

    except Exception as e:
        logger.exception("Exception Inside create_filter_query: {}".format(e))
        filter_query = False

    return filter_query


def create_sort_query(sortField, sortOrder):
    """
    The create_sort_query function creates a json for the Elastic Search request to sort the response in either
    ascending or descending order of approval or upload date. If the sortField is not the one requested in the sort_fields
    list, the json is not created and defaults to Elastic Search sorting mechanism which is according to the search score.
    """
    try:
        sort_fields = ["uploadDate", "approval_date"]
        sort_orders = ["asc", "desc"]
        sort_query = list()
        if sortField in sort_fields and sortOrder in sort_orders:
            query = {sortField + ".keyword": {"order": sortOrder}}
            sort_query.append(query)
        else:
            sort_query = False
    except Exception as e:
        logger.exception("Exception Inside create_sort_query: {}".format(e))
        sort_query = False
    return sort_query

def get_follow_by_qid(params):
    """
    Get the all protocol number, role a user is following.
    """
    try:
        qID, db = params
        return db.query(PD_User_Protocols.userId,
                        PD_User_Protocols.protocol,
                        PD_User_Protocols.follow,
                        PD_User_Protocols.userRole,
                        PD_User_Protocols.redactProfile).filter(PD_User_Protocols.userId == qID).all()
    except Exception as e:
        logger.exception("Exception Inside get_follow_by_qid: {}".format(e))
        return False

def query_elastic(search_json_in: schemas.SearchJson, db, return_fields = return_fields):
    """
    1. Creates the search json to query Elastic Search with keyword passed, all the filters and sort query.
    2. Creates the search json to query Elastic Search with keyword passed to create the dynamic filter for Indication,
    Sponsor and Phase.
    3. Get the protocol numbers and corresponding user roles for the documents user is following.
    4. Populate the user role and follow status for the protocol results obtained.
    5. Populate the dynamic filter values in the result json.
    """
    try:
        dynamic_filter_query = dict()
        dynamic_filter_query["from"] = 0
        dynamic_filter_query["size"] = 10000
        dynamic_filter_query['query'] = dict()
        dynamic_filter_query['query']['bool'] = dict()

        search_query = dict()
        search_query["from"] = (search_json_in.pageNo - 1) * search_json_in.pageSize
        search_query["size"] = search_json_in.pageSize
        search_query['query'] = dict()
        search_query['query']['bool'] = dict()

        search_keyword_query = create_keyword_query(search_json_in, apply_toc_filter = True)
        dynamic_keyword_query = create_keyword_query(search_json_in, apply_toc_filter=False)
        if search_keyword_query:
            search_query['query']['bool']['must'] = list()
            search_query['query']['bool']['must'].append(search_keyword_query)
        if dynamic_keyword_query:
            dynamic_filter_query['query']['bool']['must'] = list()
            dynamic_filter_query['query']['bool']['must'].append(dynamic_keyword_query)

        filter_query = create_filter_query(search_json_in)
        if filter_query:
            search_query['query']['bool']['filter'] = filter_query

        sort_query = create_sort_query(search_json_in.sortField, search_json_in.sortOrder)
        if sort_query:
            search_query['sort'] = sort_query

        search_query['query']['bool']['must_not'] = {"term": {"is_active": 0}}
        search_query['_source'] = return_fields

        dynamic_filter_query['query']['bool']['must_not'] = {"term": {"is_active": 0}}
        dynamic_filter_query['_source'] = ["SponsorName", "Indication", "phase"]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            user_protocols = executor.submit(get_follow_by_qid, (search_json_in.qID, db))
            es_res = executor.submit(search_elastic, search_query)
            dynamic_filter_res = executor.submit(search_elastic, dynamic_filter_query)

            user_protocols = user_protocols.result()
            es_res = es_res.result()
            dynamic_filter_res = dynamic_filter_res.result()
            executor.shutdown()

        follow_dict = {row.protocol.lower(): {'follow': row.follow, 'userRole': row.userRole, 'redactProfile': row.redactProfile} for row in user_protocols}

        res = {'ResponseCode':HTTPStatus.OK, 'Message':'Success', 'data':dict(), "count":0, "pageNo":0, "sortField":0, "total_count":0}

        if es_res:
            total_len = es_res['hits']['total']['value']
            es_res = es_res['hits']['hits']
            res["data"] = [val["_source"] for val in es_res]

            user_ids = list({data.get('UserId', '') for data in res['data'] if data.get('UserId', '')})
            user_details = user.get_by_username_list(db, user_ids)
            user_details = {user_detail.username.lower():' '.join([user_detail.first_name, user_detail.last_name]) for user_detail in user_details}

            correct_approval = list()
            incorrect_approval = list()
            for row in res['data']:
                user_protocol_detail = follow_dict.get(row.get('ProtocolNo', '').lower(), False)
                if user_protocol_detail == False:
                    row['Follow'] = False
                    row['UserRole'] = 'secondary'
                    row['redactProfile'] = config.USERROLE_REDACTPROFILE_MAP['secondary']                    
                else:
                    row['Follow'] = user_protocol_detail.get('follow', False)
                    row['UserRole'] = user_protocol_detail.get('userRole', 'secondary')
                    row['redactProfile'] = user_protocol_detail.get('redactProfile')

                row['uploadedBy'] = ''
                if row.get('UserId', ''):
                    if row['UserId'].lower().startswith(('q', 'u', 's')):
                        row['uploadedBy'] = user_details.get(row['UserId'].lower(), '')
                    else:
                        q_user_id = 'q' + row['UserId'].lower()
                        u_user_id = 'u' + row['UserId'].lower()
                        s_user_id = 's' + row['UserId'].lower()
                        uploaded_by = ''
                        if q_user_id in user_details:
                            uploaded_by = user_details.get(q_user_id, '')
                        elif u_user_id in user_details:
                            uploaded_by = user_details.get(u_user_id, '')
                        elif s_user_id in user_details:
                            uploaded_by = user_details.get(s_user_id, '')
                        row['uploadedBy'] = uploaded_by

                if row['approval_date'].isnumeric() and len(row['approval_date']) != 8:
                    row['approval_date'] = ''

                if search_json_in.sortField == 'approval_date':
                    if row['approval_date'].isnumeric() and len(row['approval_date']) == 8:
                        correct_approval.append(row)
                    else:
                        row['approval_date'] = ''
                        incorrect_approval.append(row)
            if search_json_in.sortField == 'approval_date':
                correct_approval.extend(incorrect_approval)
                res["data"] = correct_approval
            res["count"] = len(res["data"])
            res["pageNo"] = search_json_in.pageNo
            res["sortField"] = search_json_in.sortField
            res["total_count"] = total_len

        if dynamic_filter_res:
            phases = list({val['_source']['phase'] for val in dynamic_filter_res['hits']['hits'] if 'phase' in val['_source']})
            indications = list({val['_source']['Indication'] for val in dynamic_filter_res['hits']['hits'] if 'Indication' in val['_source']})
            sponsors = list({val['_source']['SponsorName'] for val in dynamic_filter_res['hits']['hits'] if 'SponsorName' in val['_source']})
            phases.sort()
            indications.sort()
            sponsors.sort()
        else:
            phases = []
            indications = []
            sponsors = []

        res["phases"] = phases
        res["indications"] = indications
        res["sponsors"] = sponsors

        # Apply redaction
        res['data'], _ = redactor.on_attributes(current_db=db, multiple_doc_attributes=res['data'])

    except Exception as ex:
        logger.exception("Exception Inside query_elastic: {}".format(ex))
        res = dict()
        res['ResponseCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
        res['Message'] = str(ex)

    return res
