import logging
from .producer_utils import confirm_produce
from .confluent_runtime_vars import env_vars
from nubium_utils.custom_exceptions import IncompatibleEnvironmentError

LOGGER = logging.getLogger(__name__)


def success_headers(headers):
    """
    Updates headers for a message when a process succeeds

    Resets the kafka_retry_count to 0,
    or adds if it didn't originally exist
    """

    try:
        headers = dict(headers)
    except TypeError:
        headers = {}

    headers['kafka_retry_count'] = '0'
    return headers


def produce_message_callback(error, message):
    """
    Logs the returned message from the Broker after producing
    NOTE: Headers not supported on the message for callback for some reason.
    NOTE: Callback requires these args
    """
    LOGGER.debug('Producer Callback...')
    if error:
        LOGGER.critical(error)
    else:
        LOGGER.debug('Producer Callback - Message produced successfully')


def consume_message_callback(error, partitions):
    """
    Logs the info returned when a successful commit is performed
    NOTE: Callback requires these args
    """
    LOGGER.debug('Consumer Callback...')
    if error:
        LOGGER.critical(error)
    else:
        LOGGER.debug('Consumer Callback - Message consumption committed successfully')


def synchronous_message_handling(producer=None, consumer=None):
    """
    Force the producer/consumer to acknowledge any outstanding, uncommitted messages.
    """
    if env_vars()['CONSUMER_ENABLE_AUTO_COMMIT'].lower() == 'true':
        raise IncompatibleEnvironmentError('CONSUMER_ENABLE_AUTO_COMMIT', 'true')
    if producer:
        LOGGER.debug('Waiting for produce to finish...')
        confirm_produce(producer)
    if consumer:
        LOGGER.debug('Waiting for commits to finalize...')
        consumer.commit(asynchronous=False)


def handle_no_messages(no_msg_exception=None, producer=None):
    """
    Since producer.poll() is typically called within the NU produce_message method, we want to acknowledge
    any outstanding produce attempts while the app has nothing to consume (and thus not actively producing/polling).
    """
    if no_msg_exception:
        LOGGER.debug(no_msg_exception)
    if producer:
        LOGGER.debug('flushing remaining producer queue')
        confirm_produce(producer)


def shutdown_cleanup(producer=None, consumer=None):
    """
    As part of shutdown, make sure all queued up produce messages are flushed, gracefully kill the consumer.
    """
    LOGGER.info('Performing graceful teardown of producer and/or consumer...')
    if consumer:
        LOGGER.debug("Shutting down consumer; no further commits can be queued or finalized.")
        consumer.close()
    if producer:
        LOGGER.debug("Sending/confirming the leftover messages in producer message queue")
        confirm_produce(producer, timeout=30)
