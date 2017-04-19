import json
import logging
import time

from kafka import KafkaConsumer

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
    CONNECT_ATTEMPTS = 20

    def __init__(self, kafka_host_port):
        self.kafka_host_port = kafka_host_port

    def consume_dresses(self):
        """Consume messages from the 'dresses' topic and add a new dress to the database."""
        self._consume(self.DRESSES_TOPIC, Dress.consume_dresses_payload)

    def consume_ratings(self):
        """Consumer messages from the 'ratings' topic and record the rating for a dress."""
        self._consume(self.RATINGS_TOPIC, Dress.consume_ratings_payload)

    def _consume(self, topic, handler):
        remaining_attempts = self.CONNECT_ATTEMPTS
        while remaining_attempts >= 0:
            try:
                # In case KafkaConsumer.poll() takes a long time: https://github.com/dpkp/kafka-python/issues/690
                consumer = KafkaConsumer(
                    topic,
                    bootstrap_servers=self.kafka_host_port,
                    group_id='{}-consumers'.format(topic),
                    # auto_offset_reset='earliest',
                    value_deserializer=lambda m: json.loads(m.decode('ascii')),
                )
                break
            except Exception as e:
                remaining_attempts -= 1
                log.warning(
                    "Failed to connect to Kafka with error '%s'. Trying %d more times." % (e, remaining_attempts)
                )
                if remaining_attempts == 0:
                    log.error("Could not connect to Kafka. Giving up.")
                    raise ConsumerSetupException(e)
                time.sleep(2)
        try:
            log.info("Starting '%s' consumer..." % topic)
            for msg in consumer:
                log.info('Processing payload with id: %s' % msg.key)
                log.debug(msg.value)
                handler(msg.value)
        except KeyboardInterrupt:
            log.warning("Stopping '%s' consumer" % topic)
            consumer.close()
        except Exception as e:
            consumer.close()
            raise RunningConsumerException(e)
