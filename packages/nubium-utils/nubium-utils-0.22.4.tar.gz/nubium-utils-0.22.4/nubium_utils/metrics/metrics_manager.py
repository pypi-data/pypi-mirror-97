"""
Container for standardized application monitoring gauges
"""
from prometheus_client import Gauge, CollectorRegistry
from .metrics_pusher import MetricsPusher
from nubium_utils.general_runtime_vars import env_vars


class MetricsManager:
    """
    Coordinates Prometheus monitoring for a Kafka client application

    Creates default gauges, and simplifies updates to them
    """

    def __init__(self, job: str = None, app: str = None, metrics_pusher: MetricsPusher = None, registry: CollectorRegistry = None):
        """
        Initializes monitor

        :param job: (str) Unique name of individual application instance
        :param app: (str) Common app name for grouping metrics
        :param registry: (CollectorRegistry) registry for prometheus metrics
        """
        if not job:
            job = env_vars()['HOSTNAME']
        if not app:
            app = env_vars()['APP_NAME']
        if not metrics_pusher:
            metrics_pusher = MetricsPusher()
        if not registry:
            registry = CollectorRegistry()

        self.job = job
        self.app = app
        self.registry = registry

        self.messages_consumed = Gauge('messages_consumed', 'Messages processed since application start', labelnames=['app', 'job', 'topic'], registry=self.registry)
        self.messages_produced = Gauge('messages_produced', 'Messages successfully produced since application start', labelnames=['app', 'job', 'topic'], registry=self.registry)
        self.message_errors = Gauge('message_errors', 'Exceptions caught when processing messages', labelnames=['app', 'job', 'exception'], registry=self.registry)
        self.external_requests = Gauge('external_requests', 'Network calls to external services', labelnames=['app', 'job', 'request_to', 'request_endpoint', 'request_type', 'is_bulk', 'status_code'], registry=self.registry)
        self.metrics_pusher = metrics_pusher

    def inc_messages_consumed(self, number_of_messages, topic):
        """
        Increases the messages_consumed gauge with default labels
        """
        self.messages_consumed.labels(self.app, self.job, topic).inc(number_of_messages)

    def inc_messages_produced(self, number_of_messages, topic):
        """
        Increases the messages_consumed gauge with default labels
        """
        self.messages_produced.labels(self.app, self.job, topic).inc(number_of_messages)

    def inc_message_errors(self, exception):
        """
        Increases the error gauge with default label and label of the exception
        """
        self.message_errors.labels(self.app, self.job, exception.__class__.__name__).inc(1)

    def inc_external_requests(self, request_to=None, request_endpoint=None, request_type=None, is_bulk=0, status_code=200):
        """
        Increases the external requests gauge.
        """
        self.external_requests.labels(self.app, self.job, request_to, request_endpoint, request_type, is_bulk, status_code).inc(1)

    def push_metrics(self):
        self.metrics_pusher.set_metrics_pod_ips()
        self.metrics_pusher.push_metrics(self.registry)
