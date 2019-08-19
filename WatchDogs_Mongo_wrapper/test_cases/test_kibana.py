import logging
import logstash
import sys

host = '35.236.16.13'

test_logger = logging.getLogger('python-logstash-logger')
test_logger.addHandler(logstash.TCPLogstashHandler(host, 5000, version=1))

test_logger.error('An error')
test_logger.info('An info')
test_logger.warning('A warning')
