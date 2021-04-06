import logging

from app import schemas
from app.utilities.config import settings
from app.utilities.elastic_utilities import search_elastic

logger = logging.getLogger(settings.LOGGER_NAME)

return_fields = ["AiDocId", "ProtocolNo", "ProtocolTitle", "SponsorName", "Indication", "DocumentStatus", "phase",
                 "approval_date", "uploadDate",
                 "MoleculeDevice", "is_active", "SourceFileName", "documentPath", "ProjectId", "VersionNumber"
                 ]


def create_keyword_query(search_json_in: schemas.SearchJson):
    try:
        if search_json_in.key is None or search_json_in.key == '':
            return False
        keyword_query = dict()
        keyword_query['multi_match'] = dict()
        keyword_query['multi_match']['query'] = search_json_in.key
        keyword_query['multi_match']['type'] = "phrase"  # Need to change this on the basis of "" for phrase
        if search_json_in.toc:
            keyword_query['multi_match']['fields'] = search_json_in.toc
        return keyword_query
    except Exception as e:
        logger.exception("Exception Inside create_keyword_query function:", e)
        return False


def create_keyword_filter_query(keyword_list, field):
    try:
        if keyword_list:
            query = {'terms': {field + '.keyword': keyword_list}}
        else:
            query = False
    except Exception as e:
        logger.exception("Exception Inside create_keyword_filter:", e)
        query = False
    return query


def create_date_range_query(dateFrom, dateTo, dateType):
    try:
        date_type_values = ["uploadDate", "approvalDate"]
        if dateType == "uploadDate" and len(dateFrom) == 8:
            dateFrom = dateFrom + "000000"
        if dateType == "uploadDate" and len(dateTo) == 8:
            dateTo = dateTo + "235959"
        if dateFrom != "" and dateTo != "" and dateType in date_type_values:
            query = {'range': {dateType: {"gte": dateFrom, "lte": dateTo}}}
        else:
            query = False
    except Exception as e:
        logger.exception("Exception Inside create_date_range_query:", e)
        query = False
    return query


def create_filter_query(search_json_in: schemas.SearchJson):
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
        # Date range filter
        query = create_date_range_query(search_json_in.dateFrom, search_json_in.dateTo, search_json_in.dateType)
        if query:
            filter_query.append(query)
        filter_query = {"bool": {"must": filter_query}}

    except Exception as e:
        logger.exception("Exception Inside create_filter_query:", e)
        filter_query = False

    return filter_query


def create_sort_query(sortField, sortOrder):
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
        logger.exception("Exception Inside create_sort_query:", e)
        sort_query = False
    return sort_query


def query_elastic(search_json_in: schemas.SearchJson):
    try:
        dynamic_filter_query = dict()
        dynamic_filter_query["from"] = (search_json_in.pageNo - 1) * search_json_in.pageSize
        dynamic_filter_query["size"] = 1000

        search_query = dict()
        search_query["from"] = (search_json_in.pageNo - 1) * search_json_in.pageSize
        search_query["size"] = search_json_in.pageSize
        search_query['query'] = dict()
        search_query['query']['bool'] = dict()

        keyword_query = create_keyword_query(search_json_in)
        if keyword_query:
            search_query['query']['bool']['must'] = list()
            search_query['query']['bool']['must'].append(keyword_query)
            dynamic_filter_query['query'] = keyword_query

        filter_query = create_filter_query(search_json_in)
        if filter_query:
            search_query['query']['bool']['filter'] = filter_query

        sort_query = create_sort_query(search_json_in.sortField, search_json_in.sortOrder)
        if sort_query:
            search_query['sort'] = sort_query

        search_query['query']['bool']['must_not'] = {"term": {"is_active": 0}}
        search_query['_source'] = return_fields
        dynamic_filter_query['_source'] = ["SponsorName", "Indication", "phase"]
        logger.info(search_query)

        res = search_elastic(search_query)
        dynamic_filter_res = search_elastic(dynamic_filter_query)
        if res:
            total_len = res['hits']['total']['value']
            res = res['hits']['hits']
            res = {"data": [val["_source"] for val in res]}
            res["count"] = len(res["data"])
            res["pageNo"] = search_json_in.pageNo
            res["sortField"] = search_json_in.sortField
            res["total_count"] = total_len
        else:
            res = False

        if dynamic_filter_res:
            phases = list({val['_source']['phase'] for val in dynamic_filter_res['hits']['hits']})
            indications = list({val['_source']['Indication'] for val in dynamic_filter_res['hits']['hits']})
            sponsors = list({val['_source']['SponsorName'] for val in dynamic_filter_res['hits']['hits']})
        else:
            phases = []
            indications = []
            sponsors = []
        res["phases"] = phases
        res["indications"] = indications
        res["sponsors"] = sponsors


    except Exception as e:
        logger.exception("Exception Inside query_elastic", e)
        res = False
    return res
