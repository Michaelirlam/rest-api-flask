from flask_restful import Resource, reqparse
from restaurants.api.data_store import restaurants

class RestaurantResource(Resource):
    def get(self):
        return restaurants