from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema

from dress_champion.models import Dress


ma = Marshmallow()


class AuthorSchema(ModelSchema):
    class Meta:
        model = Dress
