from decimal import Decimal

from dateutil.parser import parse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import DateTime, Integer, Unicode, Numeric


db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    created_on = Column(DateTime, default=db.func.now())
    updated_on = Column(DateTime, default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def get_or_create(cls, pk_name, pk_value):
        """A get_or_create method that is uses DB savepoints to avoid race conditions. Will create a new
        object if one does not exist, otherwise returns the existing object by this primary key value."""
        obj = cls.query.get(pk_value)
        if obj is not None:
            return obj
        obj = cls()
        setattr(obj, pk_name, pk_value)
        # Create a savepoint in case of race condition.
        db.session.begin_nested()
        try:
            db.session.add(obj)
            # Try to commit and release the savepoint.
            db.session.commit()
        except IntegrityError as e:
            # The insert failed due to a concurrent transaction.
            db.session.rollback()
            # Get the latest object with this pk that exists now.
            obj = cls.query.get(pk_value)
        return obj


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

    @classmethod
    def consume_dresses_payload(cls, payload: dict):
        dress = cls.get_or_create('uid', payload['id'])

        # todo: locking
        dress.activation_date = parse(payload['activation_date'])
        dress.name = payload['name']
        dress.season = payload['season']
        dress.price = Decimal(payload['price'])
        dress.images = payload['images']
        dress.brand = payload['brand']

        db.session.add(dress)
        db.session.commit()

    @classmethod
    def consume_ratings_payload(cls, payload: dict):
        dress_uid, rating = payload['dress_id'], payload['stars']
        dress = cls.get_or_create('uid', payload['dress_id'])

        # todo: locking
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


dress_promotion = db.Table('dress_promotions',
    Column('dress_uid', Unicode(length=100), ForeignKey('dresses.uid')),
    Column('promotion_id', Integer, ForeignKey('promotions.id')),
)
