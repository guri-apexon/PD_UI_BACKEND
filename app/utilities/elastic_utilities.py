import logging

from elasticsearch import Elasticsearch

from app.utilities.config import settings

logger = logging.getLogger(settings.LOGGER_NAME)


def search_elastic(search_query):
    try:
        es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}])
        res = es.search(body=search_query, index=settings.ELASTIC_INDEX)
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

def get_elastic_doc_by_id(aidocid):
    try:
        es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}])
        res = es.get(index=settings.ELASTIC_INDEX, id = aidocid)

    except Exception as e:
        logger.error("In app.utilities.elastic_utilities.update_elastic: {}".format(e))
        res = False

    es.close()
    return res
