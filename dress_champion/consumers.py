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
        self._consume(self.DRESSES_TOPIC, self._consume_dresses_message)

    def consume_ratings(self):
        """Consumer messages from the 'ratings' topic and record the rating for a dress."""
        self._consume(self.RATINGS_TOPIC, self._consume_ratings_message)

    def _consume(self, topic, handler):
        # TODO: https://github.com/dpkp/kafka-python/issues/690
        # first call to KafkaConsumer.poll() takes a long time
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.kafka_host_port,
                group_id='dress-consumers',
                # auto_offset_reset='earliest',
            )
        except Exception as e:
            raise ConsumerSetupException(e)
        try:
            for msg in consumer:
                handler(msg)
        except KeyboardInterrupt:
            log.warning("Stopping '%s' consumer" % topic)
            consumer.close()
        except Exception as e:
            consumer.close()
            raise RunningConsumerException(e)


    def _consume_dresses_message(self, msg: ConsumerRecord):
        import pdb; pdb.set_trace()

    def _consume_ratings_message(self, msg: ConsumerRecord):
        # TODO: marshmallow
        # TODO: error handling
        # TODO: log non-error not propagating
        # TODO: json value_deserializer https://kafka-python.readthedocs.io/en/master/usage.html#kafkaconsumer
        msg_dict = json.loads(msg.value.decode('utf-8'))
        payload = msg_dict['payload']
        log.error(payload['dress_id'])
        Dress.rate_dress(payload['dress_id'], payload['stars'])
