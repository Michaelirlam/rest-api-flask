from flask_restful import Resource, reqparse
from restaurants.db.models import Review
from restaurants.db.schemas import review_schema, reviews_schema
from restaurants.db import db

class ReviewResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("rating", type=int, required=True, help="Rating is required.")
    parser.add_argument("comment", type=str, required=False, help="Comments on the restaurant")

    def get(self, restaurant_id=None, review_id=None):
        if review_id:
            review = Review.query.filter_by(id=review_id, restaurant_id=restaurant_id).first_or_404()
            return review_schema.dump(review)
        else:
            reviews = Review.query.filter_by(restaurant_id=restaurant_id).all()
            return reviews_schema.dump(reviews)

    
    def post(self, restaurant_id):
        """Creates new review for passed in restaurant_id"""
        args = ReviewResource.parser.parse_args()
        new_review = Review(restaurant_id=restaurant_id, **args)
        db.session.add(new_review)
        db.session.commit()
        return review_schema.dump(new_review), 201

    
    def put(self, restaurant_id, review_id):
        args = ReviewResource.parser.parse_args()
        review = Review.query.filter_by(id=review_id, restaurant_id=restaurant_id).first_or_404()
        for key, value in args.items():
            setattr(review, key, value)
        db.session.commit()
        return review_schema.dump(review), 200
    
    def delete(self, restaurant_id, review_id):
        review = Review.query.filter_by(id=review_id, restaurant_id=restaurant_id).first_or_404()
        deleted_review = review_schema.dump(review)
        db.session.delete(review)
        db.session.commit()
        return {"message": "Review deleted", "review": deleted_review}