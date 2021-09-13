import logging
from datetime import datetime

from app.utilities.config import settings
from elasticsearch import Elasticsearch, helpers

logger = logging.getLogger(settings.LOGGER_NAME)


def search_elastic(search_query):
    try:
        es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}])
        res = es.search(body=search_query, index=settings.ELASTIC_INDEX, request_timeout=40)
    except Exception as e:
        logger.exception("In app.utilities.elastic_utilities.search_elastic: {}".format(e))
        res = False

    es.close()
    return res


def update_elastic(update_json, aidocid):
    try:
        es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}])
        res = es.update(index=settings.ELASTIC_INDEX, id = aidocid, body = update_json)

    except Exception as e:
        logger.exception("In app.utilities.elastic_utilities.update_elastic: {}".format(e))
        res = False

    es.close()
    return res

def update_bulk_elastic(es_update_dict: dict):
    current_timestamp = datetime.utcnow()
    current_utc_num_format = current_timestamp.strftime("%Y%m%d%H%M%S")
    return_code = True
    success_num = -1
    failures = []
    try:
        es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}])
        es_sync =   [
                        {
                        '_id': aidoc_id, 
                        '_index': settings.ELASTIC_INDEX,
                        "_source": {'doc': dict({'TimeUpdated': current_utc_num_format}, **update_fields)}, 
                        '_op_type': 'update'
                        } 
                        for aidoc_id, update_fields in es_update_dict.items()
                    ]
        logger.info(f"Bulk update attempt for {len(es_sync)} documents")
        success_num, failures = helpers.bulk(client=es, actions=es_sync, request_timeout=600, raise_on_error=False)
        logger.info(f"Successfully updated docs #: {success_num}; Failure doc #: {len(failures)}; Details: {failures}")
    except Exception as exc:
        logger.exception(f"update_bulk_elastic: {exc}")
        return_code = False
    finally:
        es.close()
    
    return return_code, success_num, failures


def get_elastic_doc_by_id(aidocid):
    try:
        es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}])
        res = es.get(index=settings.ELASTIC_INDEX, id = aidocid)

    except Exception as e:
        logger.error("In app.utilities.elastic_utilities.update_elastic: {}".format(e))
        res = False

    es.close()
    return res
