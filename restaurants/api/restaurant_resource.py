from flask_restful import Resource, reqparse, abort
from restaurants.db.models import Restaurant
from restaurants.db.schemas import restaurant_schema, restaurants_schema
from restaurants.db import db

class RestaurantResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="Name is required")
    parser.add_argument("address", type=str, required=False, help="Address of the restaurant")

    def get(self, restaurant_id=None):
        """Gets restaurant if restaurant_id is provided, else gets all restaurants
        ---
        tags: ["Restaurants"]
        parameters:
          - name: restaurant_id
            in: path
            type: integer
            required: false
            description: ID of the restaurant to retrieve
            schema:
              type: integer
        responses:
          200:
            description: Returns a restaurant or list of restaurants
          404:
            description: Restaurant not found if restaurant_id is provided
          500:
            description: Internal server error
        """
        if restaurant_id:
            # Query restaurant and return if found else return a 404 status code
            restaurant = Restaurant.query.get(restaurant_id)
            if not restaurant:
                abort(404, message="Restaurant not found.")
            return restaurant_schema.dump(restaurant), 200
        # Query all restaurants
        all_restaurants = Restaurant.query.all()
        return restaurants_schema.dump(all_restaurants), 200
 
    def post(self):
        """Creates new restaurant
        ---
        tags: ["Restaurants"]
        parameters:
          - in: body
            name: restaurant
            description: Restaurant object to be created
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: Name of the restaurant
                address:
                  type: string
                  description: Address of the restaurant
        responses:
          201:
            description: Restaurant created successfully
          400:
            description: Bad request if required fields are missing
          500:
            description: Internal server error
        """
        args =  RestaurantResource.parser.parse_args()
        new_restaurant = Restaurant(**args)
        # Adds new restaurant to the session and commits it to the database
        db.session.add(new_restaurant)
        db.session.commit()
        return restaurant_schema.dump(new_restaurant), 201
    
    def put(self, restaurant_id):
        """Updates an existing restaurant
        ---
        tags: ["Restaurants"]
        parameters:
          - in: path
            name: restaurant_id
            type: integer
            required: true
            description: ID of the restaurant to update
          - in: body
            name: restaurant
            description: Restaurant object with updated fields
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: Updated name of the restaurant
                address:
                  type: string
                  description: Updated address of the restaurant
        responses:
          200:
            description: Restaurant updated successfully
          404:
            description: Restaurant not found if restaurant_id is provided
          400:
            description: Bad request if required fields are missing
          500:
            description: Internal server error
        """
        args = RestaurantResource.parser.parse_args()
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            abort(404, message="Restaurant not found.")
        for key, value in args.items():
            setattr(restaurant, key, value)
        db.session.commit()
        return restaurant_schema.dump(restaurant), 200


    def delete(self, restaurant_id):
        """Deletes a restaurant by ID
        ---
        tags: ["Restaurants"]
        parameters:
          - in: path
            name: restaurant_id
            type: integer
            required: true
            description: ID of the restaurant to delete
        responses:
          200:
            description: Restaurant deleted successfully
          404:
            description: Restaurant not found if restaurant_id is provided
          500:
            description: Internal server error
        """
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            abort(404, message="Restaurant not found.")
        deleted_data = restaurant_schema.dump(restaurant)
        db.session.delete(restaurant)
        db.session.commit()
        return {"message": "Restaurant deleted.", "restaurant": deleted_data}, 200