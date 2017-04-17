import logging
import sys

from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_script.commands import InvalidCommand

from dress_champion import create_app
from dress_champion.consumers import DressConsumer, DressConsumerException


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)


@manager.command
def consume(topic):
    consumer = DressConsumer(manager.app.config['KAFKA_HOST_PORT'])
    try:
        if topic == DressConsumer.DRESSES_TOPIC:
            consumer.consume_dresses()
        elif topic == DressConsumer.RATINGS_TOPIC:
            consumer.consume_ratings()
        else:
            log.error("Invalid topic provided: %s" % topic)
            raise InvalidCommand

    except DressConsumerException as e:
        log.error("Error consuming %s: %s" % (topic, e))
        raise InvalidCommand


if __name__ == '__main__':
    try:
        manager.run()
    except InvalidCommand as err:
        sys.exit(1)
