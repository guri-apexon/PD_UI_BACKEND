import logging

from elasticsearch import Elasticsearch

from app.utilities.config import settings

logger = logging.getLogger(settings.LOGGER_NAME)


def search_elastic(search_query):
    try:
        es = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}])
        res = es.search(body=search_query, index=settings.ELASTIC_INDEX)
    except Exception as e:
        logger.exception("In app.utilities.elastic_utilities.search_elastic:", e)
        res = False

    es.close()
    return res
