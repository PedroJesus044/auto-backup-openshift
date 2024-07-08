import logstash, sys, logging

host = 'localhost'

test_logger = logging.getLogger('python-logstash-logger')

test_logger.setLevel(logging.INFO)
handler = logstash.LogstashHandler(host, 5000, version=1)
#handler.setFormatter(logging.Formatter)
test_logger.addHandler(handler)

extra = {
    'respaldo':"Siara - Paralelo"
}