from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import DateTime, Integer, Unicode, Numeric
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm.attributes import flag_modified


db = SQLAlchemy()


class Dress(db.Model):
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
    def add_new_dress(cls):
        # from dress_champion.schemas import AuthorSchema
        dress = cls.query.get(dress_uid)



    @classmethod
    def rate_dress(cls, dress_uid, rating):
        dress = cls.query.get(dress_uid)
        if dress is None:
            dress = cls(uid=dress_uid)

        ratings = dress.ratings if dress.ratings else []
        ratings.append(rating)
        dress.ratings = ratings
        # http://stackoverflow.com/a/34339963/1153746
        flag_modified(dress, 'ratings')

        db.session.add(dress)
        db.session.commit()


class Promotion(db.Model):
    __tablename__ = 'promotions'

    id = Column(Integer, primary_key=True)


dress_promotion = db.Table('dress_promotions',
    Column('dress_uid', Unicode(length=100), ForeignKey('dresses.uid')),
    Column('promotion_id', Integer, ForeignKey('promotions.id')),
)
