from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from dress_champion.models import Dress


ma = Marshmallow()


class DressSchema(ModelSchema):
    class Meta:
        model = Dress

    stars = fields.Decimal()


dress_schema = DressSchema()
dresses_schema = DressSchema(many=True)
