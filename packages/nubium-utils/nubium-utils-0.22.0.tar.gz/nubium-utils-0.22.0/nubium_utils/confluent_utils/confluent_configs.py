import logging
from .message_utils import produce_message_callback, consume_message_callback
from nubium_utils.metrics import start_pushing_metrics
from .confluent_runtime_vars import env_vars

LOGGER = logging.getLogger(__name__)


def init_ssl_configs():
    """
    Provides producer or consumer SSL configs.
    :return: config params
    :rtype: dict
    """
    if env_vars()['USE_SSL'].lower() == 'true':
        LOGGER.info('Initializing producers and consumers with TLS configurations ENABLED.')

        if env_vars()["USE_SASL"].lower() == 'true':
            LOGGER.info('Initializing producers and consumers with SASL')
            return {
                "security.protocol": "sasl_ssl",
                "sasl.mechanisms": "PLAIN",
                "sasl.username": env_vars()["SASL_USERNAME"],
                "sasl.password": env_vars()["SASL_PASSWORD"]
            }
        else:
            LOGGER.info('Initializing producers and consumers with SSL')
            return {
                "security.protocol": "ssl",
                "ssl.ca.location": env_vars()["SSL_CA_LOCATION"],
                "ssl.certificate.location": env_vars()["SSL_CERTIFICATE_LOCATION"],
                "ssl.key.location": env_vars()["SSL_KEY_LOCATION"]}
    else:
        LOGGER.info('Initializing producers and consumers with TLS configurations DISABLED.')
    return {}


def init_schema_registry_configs():
    """
    Provides the avro schema config
    :return: dict, None
    """
    url = env_vars()['SCHEMA_REGISTRY_URL']
    if url:
        LOGGER.info(f'Using the schema server at {url}')
        return {'schema.registry.url': url}
    else:
        LOGGER.info(f'No schema registry URL provided; schema registry usage DISABLED')
        return None


def init_producer_configs(ssl_configs=None, schema_registry_configs=None):
    """
    Provides producer config.
    :return: config params
    :rtype: dict
    """
    if not ssl_configs:
        ssl_configs = {}
    if not schema_registry_configs:
        schema_registry_configs = {}
    return {
        **ssl_configs,
        **schema_registry_configs,
        "bootstrap.servers": env_vars()['KAFKA_CLUSTER'],
        "on_delivery": produce_message_callback,
        "acks": "all"}


def init_consumer_configs(ssl_configs=None, schema_registry_configs=None):
    """
    Provides consumer config.
    :return: config params
    :rtype: dict
    """
    if not ssl_configs:
        ssl_configs = {}
    if not schema_registry_configs:
        schema_registry_configs = {}
    max_time_between_consumes_mins = int(env_vars()['CONSUMER_TIMEOUT_LIMIT_MINUTES']) + int(env_vars()['TIMESTAMP_OFFSET_MINUTES'])
    return {
        **ssl_configs,
        **schema_registry_configs,
        "bootstrap.servers": env_vars()['KAFKA_CLUSTER'],
        "group.id": env_vars()['APP_NAME'],
        "on_commit": consume_message_callback,
        "enable.auto.commit": env_vars()['CONSUMER_ENABLE_AUTO_COMMIT'],
        "max.poll.interval.ms": str(60000 * max_time_between_consumes_mins),
        "message.max.bytes": env_vars()['MESSAGE_BATCH_MAX_MB'],
        "fetch.max.bytes": env_vars()['MESSAGE_TOTAL_MAX_MB'],
        "queued.max.messages.kbytes": env_vars()['MESSAGE_QUEUE_MAX_MB']}


def init_metrics_pushing(metrics_manager):
    if env_vars()['DO_METRICS_PUSHING'].lower() == 'true':
        LOGGER.info('Metric pushing to gateway ENABLED')
        start_pushing_metrics(metrics_manager, int(env_vars()['METRICS_PUSH_RATE']))
    else:
        LOGGER.info('Metric pushing to gateway DISABLED')
