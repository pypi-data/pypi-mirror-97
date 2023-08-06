import unittest
from unittest import mock
import socket

from prometheus_client import CollectorRegistry

from nubium_utils.metrics import MetricsManager, MetricsPusher


class TestMonitor(unittest.TestCase):

    def test_metrics_manager_init(self):
        """
        A metrics_manager initialized with all of it's arguments should succeed
        """
        metrics_manager = MetricsManager(job='test', app='test', registry=CollectorRegistry(), metrics_pusher=mock.MagicMock())
        assert metrics_manager

    def test_registry_auto_create(self):
        """
        When a metrics_manager is created without a registry arg, it initializes one
        """
        metrics_manager = MetricsManager(job='test', app='test', metrics_pusher=mock.MagicMock())
        assert metrics_manager.registry.__class__ == CollectorRegistry

    def test_gauge_creation(self):
        """
        The metrics_manager class should create 3 gauges with specific labels
        """
        metrics_pusher = mock.MagicMock()
        metrics_manager = MetricsManager(job='test', app='test', metrics_pusher=metrics_pusher)

        assert metrics_manager.messages_consumed._labelnames == ('app', 'job', 'topic')
        assert metrics_manager.message_errors._labelnames == ('app', 'job', 'exception')
        assert metrics_manager.messages_produced._labelnames == ('app', 'job', 'topic')

    def test_increment_gauges(self):
        """
        A utility function should increment gauges with specific label values
        """
        metrics_manager = MetricsManager(job='test-job', app='test-app', metrics_pusher=mock.MagicMock())
        metrics_manager.inc_messages_consumed(1, 'test-topic')
        assert metrics_manager.messages_consumed._metrics[('test-app', 'test-job', 'test-topic')]._value._value == 1

        metrics_manager.inc_messages_produced(1, 'test-topic')
        assert metrics_manager.messages_produced._metrics[('test-app', 'test-job', 'test-topic')]._value._value == 1

    def test_increment_message_errors(self):
        """
        Method should increase metric with matching exception label value
        """
        metrics_manager = MetricsManager(job='test-job', app='test-app', metrics_pusher=mock.MagicMock())
        metrics_manager.inc_message_errors(ValueError('test-value-error'))
        assert metrics_manager.message_errors._metrics[('test-app', 'test-job', 'ValueError')]._value._value == 1


class TestMetricsPusher(unittest.TestCase):
    """
    Tests for the class that manages pushing metrics to a metrics cache
    """

    def test_initialization(self):
        """
        Class should initialize with correct arguments
        """
        metrics_pusher = MetricsPusher('test-job', 'test-service-name', 'test-service-port', 'test-pod-port')
        assert metrics_pusher is not None

    def test_set_gateways(self):
        """
        Set gateways returns 2 IP addresses when called with mocked values
        """

        metrics_pusher = MetricsPusher('test-job', 'test-service-name', 'test-service-port', 'test-pod-port')

        # Mock out the socket.getaddrinfo call return value
        addrinfo_mock = [
            (socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_DGRAM, 17, '', ('127.0.0.1', 8080)),
            (socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_DGRAM, 6, '', ('127.0.0.1', 8080)),
            (socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_DGRAM, 17, '', ('127.0.0.2', 8080)),
            (socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_DGRAM, 6, '', ('127.0.0.2', 8080)),
        ]

        with mock.patch('nubium_utils.metrics.metrics_pusher.socket') as socket_patch:
            socket_patch.getaddrinfo.return_value = addrinfo_mock
            metrics_pusher.set_metrics_pod_ips()
            assert metrics_pusher.metrics_pod_ips == {'127.0.0.1:test-pod-port', '127.0.0.2:test-pod-port'}

    def test_push_metrics(self):
        """
        Assert that the push metrics function is called for every gateway
        """

        metrics_pusher = MetricsPusher('test-job', 'test-service-name', 'test-service-port', 'test-pod-port')

        metrics_pusher.metrics_pod_ips = {
            'test-ip-address-1:test-port',
            'test-ip-address-2:test-port'
        }

        with mock.patch('nubium_utils.metrics.metrics_pusher.push_to_gateway') as push_to_gateway_patch:
            registry = CollectorRegistry()
            metrics_pusher.push_metrics(registry)
            assert unittest.mock.call('test-ip-address-1:test-port', job='test-job', registry=registry, timeout=15) in push_to_gateway_patch.call_args_list
            assert unittest.mock.call('test-ip-address-2:test-port', job='test-job', registry=registry, timeout=15) in push_to_gateway_patch.call_args_list
