import json
import logging
from typing import Optional

from rasa.core.brokers.event_channel import EventChannel
from rasa.utils.io import DEFAULT_ENCODING

logger = logging.getLogger(__name__)


class KafkaProducer(EventChannel):
    def __init__(
        self,
        host,
        sasl_username=None,
        sasl_password=None,
        ssl_cafile=None,
        ssl_certfile=None,
        ssl_keyfile=None,
        ssl_check_hostname=False,
        topic="rasa_core_events",
        security_protocol="SASL_PLAINTEXT",
        loglevel=logging.ERROR,
    ):
        if host and ',' in host:
            self.host = host.split(",")
        else:
            self.host = host
        self.topic = topic
        self.security_protocol = security_protocol
        self.sasl_username = sasl_username
        self.sasl_password = sasl_password
        self.ssl_cafile = ssl_cafile
        self.ssl_certfile = ssl_certfile
        self.ssl_keyfile = ssl_keyfile
        self.ssl_check_hostname = ssl_check_hostname
        self.producer = self._create_producer()

        logging.getLogger("kafka").setLevel(loglevel)

    @classmethod
    def from_endpoint_config(cls, broker_config) -> Optional["KafkaProducer"]:
        if broker_config is None:
            return None

        return cls(broker_config.url, **broker_config.kwargs)

    def publish(self, event):
        # self._create_producer()
        self._publish(event)
        # self._close()

    def _create_producer(self):
        import kafka

        if self.security_protocol == "SASL_PLAINTEXT":
            return kafka.KafkaProducer(
                bootstrap_servers=self.host,
                value_serializer=lambda v: json.dumps(v).encode(DEFAULT_ENCODING),
                sasl_plain_username=self.sasl_username,
                sasl_plain_password=self.sasl_password,
                sasl_mechanism="PLAIN",
                security_protocol=self.security_protocol,
            )
        elif self.security_protocol == "SSL":
            return kafka.KafkaProducer(
                bootstrap_servers=self.host,
                value_serializer=lambda v: json.dumps(v).encode(DEFAULT_ENCODING),
                ssl_cafile=self.ssl_cafile,
                ssl_certfile=self.ssl_certfile,
                ssl_keyfile=self.ssl_keyfile,
                ssl_check_hostname=False,
                security_protocol=self.security_protocol,
            )
        elif self.security_protocol == "PLAINTEXT":
            return kafka.KafkaProducer(
                bootstrap_servers=self.host,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
        else:
            return None

    def _publish(self, event):
        # self.producer.send(self.topic, event)
        if event.get('sender_id'):
            self.producer.send(self.topic, value=event, key=bytes(event.get('sender_id'), 'utf-8'))
        else:
            self.producer.send(self.topic, event)

    def _close(self):
        self.producer.close()

    def is_connected(self):
        producer = self._create_producer()
        is_connected = producer.bootstrap_connected()
        producer.close()
        return is_connected

    def flush(self):
        self.producer.flush(30)