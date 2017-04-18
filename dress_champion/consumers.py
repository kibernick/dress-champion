import json
import logging

from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord

from dress_champion.models import Dress


log = logging.getLogger(__name__)


class DressConsumerException(Exception):
    pass


class ConsumerSetupException(DressConsumerException):
    pass


class RunningConsumerException(DressConsumerException):
    pass


class DressConsumer:

    DRESSES_TOPIC = 'dresses'
    RATINGS_TOPIC = 'ratings'

    def __init__(self, kafka_host_port):
        self.kafka_host_port = kafka_host_port

    def consume_dresses(self):
        """Consume messages from the 'dresses' topic and add a new dress to the database."""
        self._consume(self.DRESSES_TOPIC, Dress.consume_dresses_payload)

    def consume_ratings(self):
        """Consumer messages from the 'ratings' topic and record the rating for a dress."""
        self._consume(self.RATINGS_TOPIC, Dress.consume_ratings_payload)

    def _consume(self, topic, handler):
        # TODO: https://github.com/dpkp/kafka-python/issues/690
        # first call to KafkaConsumer.poll() takes a long time
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.kafka_host_port,
                group_id='{}-consumers'.format(topic),
                # auto_offset_reset='earliest',
                value_deserializer=lambda m: json.loads(m.decode('ascii')),
            )
        except Exception as e:
            raise ConsumerSetupException(e)
        try:
            log.info("Starting '%s' consumer..." % topic)
            for msg in consumer:  # type: ConsumerRecord
                log.info('Processing payload with id: %s' % msg.key)
                handler(msg.value['payload'])
        except KeyboardInterrupt:
            log.warning("Stopping '%s' consumer" % topic)
            consumer.close()
        except Exception as e:
            consumer.close()
            raise RunningConsumerException(e)
