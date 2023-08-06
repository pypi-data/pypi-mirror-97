from prometheus_client import Counter
from prometheus_client import multiprocess, start_http_server, Gauge, Counter


class Prom:
    core_endpoint_get_health_count = Counter('my_start', 'Description of counter')