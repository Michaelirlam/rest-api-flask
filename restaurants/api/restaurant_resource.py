from flask_restful import Resource, reqparse
from restaurants.api.data_store import restaurants
from restaurants.db.models import Restaurant
from restaurants.db.schemas import restaurant_schema, restaurants_schema
from restaurants.db import db

class RestaurantResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="Name is required")
    parser.add_argument("address", type=str, required=False, help="Address of the restaurant")

    def get(self, restaurant_id=None):
        """Gets restaurant if restaurant_id is provided, else gets all restaurants"""
        if restaurant_id:
            # Query restaurant and return if found else return a 404 status code
            restaurant = Restaurant.query.get_or_404(restaurant_id)
            return restaurant_schema.dump(restaurant)
        # Query all restaurants
        all_restaurants = Restaurant.query.all()
        return restaurants_schema.dump(all_restaurants)
    
    def post(self):
        """Creates new restaurant"""
        args =  RestaurantResource.parser.parse_args()
        new_restaurant = Restaurant(**args)
        # Adds new restaurant to the session and commits it to the database
        db.session.add(new_restaurant)
        db.session.commit()
        return restaurant_schema.dump(new_restaurant), 201
    
    def put(self, restaurant_id):
        args = RestaurantResource.parser.parse_args()
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        for key, value in args.items():
            setattr(restaurant, key, value)
        db.session.commit()
        return restaurant_schema.dump(restaurant)


    def delete(self, restaurant_id):
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        deleted_data = restaurant_schema.dump(restaurant)
        db.session.delete(restaurant)
        db.session.commit()
        return {"message": "Restaurant deleted.", "restaurant":{deleted_data}}, 200