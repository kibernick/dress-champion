from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from dress_champion.models import Dress, Promotion


ma = Marshmallow()


class DressSchema(ModelSchema):
    class Meta:
        model = Dress

    stars = fields.Decimal()


class PromotionSchema(ModelSchema):
    class Meta:
        model = Promotion


dress_schema = DressSchema()
dresses_schema = DressSchema(many=True)

promotion_schema = PromotionSchema()
promotions_schema = PromotionSchema(many=True)
