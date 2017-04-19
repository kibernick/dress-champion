import flask_restless

from dress_champion.models import Dress


api = flask_restless.APIManager()

api.create_api(Dress, methods=['GET'], primary_key='uid', results_per_page=10)
