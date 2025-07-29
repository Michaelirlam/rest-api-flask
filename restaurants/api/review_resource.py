from flask_restful import Resource, reqparse
from restaurants.db.models import Review
from restaurants.db.schemas import review_schema, reviews_schema
from restaurants.db import db

class ReviewResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("rating", type=int, required=True, help="Rating is required.")
    parser.add_argument("comment", type=str, required=False, help="Comments on the restaurant")

    def get(self, restaurant_id=None, review_id=None):
        """Gets reviews for a restaurant or a specific review if review_id is provided
        ---
        tags: ["Reviews"]
        parameters:
          - name: restaurant_id
            in: path
            type: integer
            required: true
            description: ID of the restaurant to retrieve reviews for
          - name: review_id
            in: path
            type: integer
            required: false
            description: ID of the review to retrieve
            schema:
              type: integer
        responses:
          200:
            description: Returns a review or list of reviews
          404:
            description: Review not found if review_id is provided
          500:
            description: Internal server error
        """
        if not restaurant_id:
            return {"message": "Restaurant ID is required to retrieve reviews"}, 400
        if review_id:
            review = Review.query.filter_by(id=review_id, restaurant_id=restaurant_id).first_or_404()
            return review_schema.dump(review)
        else:
            reviews = Review.query.filter_by(restaurant_id=restaurant_id).all()
            return reviews_schema.dump(reviews)

    
    def post(self, restaurant_id):
        """Creates a new review for a restaurant
        ---
        tags: ["Reviews"]
        parameters:
          - in: body
            name: review
            description: Review object to be created
            required: true
            schema:
              type: object
              properties:
                rating:
                  type: integer
                  description: Rating of the restaurant
                comment:
                  type: string
                  description: Comments on the restaurant
        responses:
          201:
            description: Review created successfully
          400:
            description: Bad request if required fields are missing
          500:
            description: Internal server error
        """
        if not restaurant_id:
            return {"message": "Restaurant ID is required to create a review"}, 400
        args = ReviewResource.parser.parse_args()
        new_review = Review(restaurant_id=restaurant_id, **args)
        db.session.add(new_review)
        db.session.commit()
        return review_schema.dump(new_review), 201

    def put(self, restaurant_id, review_id):
        """Updates an existing review
        ---
        tags: ["Reviews"]
        parameters:
          - name: restaurant_id
            in: path
            type: integer
            required: true
            description: ID of the restaurant to which the review belongs
          - name: review_id
            in: path
            type: integer
            required: true
            description: ID of the review to update
          - in: body
            name: review
            description: Review object with updated fields
            required: true
            schema:
              type: object
              properties:
                rating:
                  type: integer
                  description: Updated rating of the restaurant
                comment:
                  type: string
                  description: Updated comments on the restaurant
        responses:
          200:
            description: Review updated successfully
          404:
            description: Review not found if review_id is provided
          400:
            description: Bad request if required fields are missing
          500:
            description: Internal server error
        """
        if not review_id:
            return {"message": "Review ID is required for update"}, 400
        args = ReviewResource.parser.parse_args()
        review = Review.query.filter_by(id=review_id, restaurant_id=restaurant_id).first_or_404()
        for key, value in args.items():
            setattr(review, key, value)
        db.session.commit()
        return review_schema.dump(review), 200
    
    def delete(self, restaurant_id, review_id):
        """Deletes a review by ID
        ---
        tags: ["Reviews"]
        parameters:
          - name: restaurant_id
            in: path
            type: integer
            required: true
            description: ID of the restaurant to which the review belongs
          - name: review_id
            in: path
            type: integer
            required: true
            description: ID of the review to delete
        responses:
          200:
            description: Review deleted successfully
          404:
            description: Review not found if review_id is provided
          500:
            description: Internal server error
        """
        if not review_id:
            return {"message": "Review ID is required for deletion"}, 400
        if not restaurant_id:
            return {"message": "Restaurant ID is required for deletion"}, 400
        review = Review.query.filter_by(id=review_id, restaurant_id=restaurant_id).first_or_404()
        deleted_review = review_schema.dump(review)
        db.session.delete(review)
        db.session.commit()
        return {"message": "Review deleted", "review": deleted_review}