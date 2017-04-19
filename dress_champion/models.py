import logging
from decimal import Decimal

import pytz
from dateutil.parser import parse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import DateTime, Integer, Unicode, Numeric

db = SQLAlchemy()
log = logging.getLogger(__name__)


class Base(db.Model):
    """Abstract base class for our models."""
    __abstract__ = True

    created_on = Column(DateTime, default=db.func.utc_timestamp())
    updated_on = Column(DateTime, default=db.func.utc_timestamp(), onupdate=db.func.utc_timestamp())

    @classmethod
    def get_or_create(cls, pk_name, pk_value):
        """A get_or_create method that is uses DB savepoints to avoid race conditions. Will create a new
        object if one does not exist, otherwise returns the existing object by this primary key value.
        
        Returns:
            object: Instance of the model queried/created.
            bool: Was a new instance created or not.
        
        """
        obj = cls.query.get(pk_value)
        if obj is not None:
            return obj, False
        obj = cls()
        setattr(obj, pk_name, pk_value)
        try:
            db.session.add(obj)
            db.session.commit()
            return obj, True
        except Exception as e:
            log.warning('The insert failed due to a concurrent transaction: {}'.format(pk_value))
            db.session.rollback()
            # Get the latest object with this pk that exists now.
            obj = cls.query.get(pk_value)
            assert obj is not None, "Error retrieving <{}: {}>".format(cls.__name__, pk_value)
            return cls.query.get(pk_value), False


def coerce_to_utc(datetime_str):
    try:
        dt = parse(datetime_str)
    except (TypeError, ValueError):
        return None
    if dt is not None and dt.tzinfo is not None:
        # Convert any existing timezone information to UTC.
        dt = dt.astimezone(pytz.UTC)
    return dt


class Dress(Base):
    __tablename__ = 'dresses'

    uid = Column(Unicode(length=100), primary_key=True)

    activation_date = Column(DateTime)
    name = Column(Unicode(length=255))
    season = Column(Unicode(length=20))
    price = Column(Numeric)

    images = Column(JSON)
    brand = Column(JSON)
    ratings = Column(JSON)

    def __repr__(self):
        return "<Dress: {}>".format(self.uid)

    @classmethod
    def consume_dresses_payload(cls, msg):
        # todo: locking
        payload = msg.get('payload')
        if not payload:
            log.warning('Missing payload.')
            return

        dress, _ = cls.get_or_create('uid', payload['id'])
        updates = {
            'activation_date': coerce_to_utc(payload['activation_date']),
            'name': payload.get('name'),
            'season': payload.get('season'),
            'price': Decimal(payload['price']) if payload.get('price') else None,
            'images': payload.get('images'),
            'brand': payload.get('brand'),
        }
        for attr, value in updates.items():
            if value is not None:
                setattr(dress, attr, value)

        db.session.add(dress)
        db.session.commit()

    @classmethod
    def consume_ratings_payload(cls, msg):
        # todo: locking
        payload = msg.get('payload')
        if not payload:
            log.warning('Missing payload.')
            return

        dress_uid, rating = payload['dress_id'], payload['stars']
        dress, _ = cls.get_or_create('uid', payload['dress_id'])

        ratings = dress.ratings if dress.ratings else []
        ratings.append(rating)
        dress.ratings = ratings
        # http://stackoverflow.com/a/34339963/1153746
        flag_modified(dress, 'ratings')

        db.session.add(dress)
        db.session.commit()


class Promotion(Base):
    __tablename__ = 'promotions'

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return "<Promotion: {}>".format(self.id)


dress_promotion = db.Table('dress_promotions',
    Column('dress_uid', Unicode(length=100), ForeignKey('dresses.uid')),
    Column('promotion_id', Integer, ForeignKey('promotions.id')),
)
