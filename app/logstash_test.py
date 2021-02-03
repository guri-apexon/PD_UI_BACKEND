import logging
import sys
from logstash_async.handler import AsynchronousLogstashHandler

host = 'ca2spdml01q'
port = 5959

#test_logger = logging.getLogger('python-logstash-logger')
logger = logging.getLogger('pd-ui-backend')
logger.setLevel(logging.INFO)
logger.addHandler(AsynchronousLogstashHandler(
    host, port, database_path='logstash.db'))

# If you don't want to write to a SQLite database, then you do
# not have to specify a database_path.
# NOTE: Without a database, messages are lost between process restarts.
# test_logger.addHandler(AsynchronousLogstashHandler(host, port))

logger.error('python-logstash-async: test logstash error message.')
logger.info('python-logstash-async: test logstash info message.')
logger.warning('python-logstash-async: test logstash warning message.')

# add extra field to logstash message
extra = {
    'test_string': 'python version: ' + repr(sys.version_info),
    'test_boolean': True,
    'test_dict': {'a': 1, 'b': 'c'},
    'test_float': 1.23,
    'test_integer': 123,
    'test_list': [1, 2, '3'],
}
logger.info('python-logstash: test extra fields', extra=extra)