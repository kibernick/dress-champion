import flask_restless

from dress_champion.models import db, Dress


api = flask_restless.APIManager(flask_sqlalchemy_db=db)

api.create_api(Dress, methods=['GET'], additional_attributes=['stars'])
