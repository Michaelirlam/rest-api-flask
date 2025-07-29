from db.models import Restaurant, Review
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class RestaurantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Restaurant
        include_relationships = True
        load_instance = True

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        include_fk = True
        load_instance = True

restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)