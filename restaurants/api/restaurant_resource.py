from flask_restful import Resource, reqparse
from restaurants.api.data_store import restaurants

class RestaurantResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="Name is required")
    parser.add_argument("address", type=str, required=False, help="Address of the restaurant")

    def get(self, restaurant_id=None):
        """returns restaurant by id if one was passed in, else returns all restaurants"""
        if restaurant_id:
            # Find the restaurant by its ID
            restaurant = next((r for r in restaurants if r["id"] == restaurant_id), None)
            if restaurant:
                return restaurant, 200
            return {"message": "Restaurant not fount"}, 404
        return restaurants
    
    def post(self):
        """Creates new restaurant"""
        args =  RestaurantResource.parser.parse_args()
        new_id = max(r["id"] for r in restaurants) + 1 if restaurants else 1
        new_restaurant = {"id": new_id, "name": args["name"], "address": args["address"]}
        restaurants.append(new_restaurant)
        return new_restaurant, 201
    
    def put(self, restaurant_id):
        args = RestaurantResource.parser.parse_args()
        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                if args["name"]:
                    restaurant["name"] = args["name"]
                if args["address"]:
                    restaurant["address"] = args["address"]
                return restaurant, 200
        return {"message": "Restaurant not found."}, 404

    def delete(self, restaurant_id):
        global restaurants
        for i, restaurant in enumerate(restaurants):
            if restaurant["id"] == restaurant_id:
                del restaurants[i]
                return "", 200
        return {"message": "Restaurant not found."}