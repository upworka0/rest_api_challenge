"""Usage resource for handling any usage requests"""

from flask import jsonify
from flask_restful import Resource

from src.models.utils import get_object_or_404
from src.schemas.usage import UsageSchema

from src.tasks.usage import *


class UsageAPI(Resource):
    """Resource/routes for Usage endpoints"""

    def get(self, sid):
        """External facing usage endpoint GET

        Gets an existing Usage object by sid

        Args:
            sid (int): id of usage object

        Returns:
            json: serialized usage object

        """
        subscription = get_object_or_404(Subscription, sid)
        usages = get_current_usages(subscription)

        result = UsageSchema().dump(usages, many=True)
        res_data = {
            "usages": result.data,
            "usage_status": not check_subscription(subscription)
        }
        check_subscriptions()
        return jsonify(res_data)
