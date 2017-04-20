import logging

import flask_restless
import flask_restful

from dress_champion.models import db, Dress, Promotion
from dress_champion.schemas import promotion_schema


log = logging.getLogger(__name__)


# Auto-generated API endpoints based on SQLAlchemy models.

restless_api = flask_restless.APIManager(flask_sqlalchemy_db=db)

restless_api.create_api(Dress, methods=['GET'], additional_attributes=['stars'])
"""List and query Dresses."""

restless_api.create_api(Promotion, methods=['GET', 'POST', 'PUT'])
"""List and create Promotions."""


# Customizable API endpoints.

def get_or_abort(model, id):
    """Retrieve an instance of model or raise HTTP 404."""
    instance = model.query.get(id)
    if instance is None:
        flask_restful.abort(404, message="{} {} doesn't exist".format(model.__name__, id))
    return instance


class DressPromotion(flask_restful.Resource):

    def post(self, promo_id, dress_id):
        promo = get_or_abort(Promotion, promo_id)
        dress = get_or_abort(Dress, dress_id)
        try:
            promo.dresses.append(dress)
            db.session.add(promo)
            db.session.commit()
        except Exception as e:
            err_msg = "Error adding Dress(id={}) to Promotion(id={})".format(dress_id, promo_id)
            log.error("%s %s" % (err_msg, e))
            db.session.rollback()  # todo: investigate a flask request session rollback library
            flask_restful.abort(500, message=err_msg)
        return promotion_schema.dump(promo)

    def delete(self, promo_id, dress_id):
        """Remove a dress from promotion."""
        promo = get_or_abort(Promotion, promo_id)
        dress = get_or_abort(Dress, dress_id)
        try:
            promo.dresses.remove(dress)
            db.session.add(promo)
            db.session.commit()
        except Exception as e:
            err_msg = "Error removing Dress(id={}) from Promotion(id={})".format(dress_id, promo_id)
            log.error("%s %s" % (err_msg, e))
            db.session.rollback()
            flask_restful.abort(500, message=err_msg)
        return promotion_schema.dump(promo)


restful_api = flask_restful.Api(prefix='/api')
restful_api.add_resource(DressPromotion, '/promotions/<promo_id>/dresses/<dress_id>')
