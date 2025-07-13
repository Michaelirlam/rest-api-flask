from flask_restful import Resource, reqparse
from restaurants.api.data_store import restaurants

class ReviewResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("rating", type=int, required=True, help="Rating is required.")
    parser.add_argument("comment", type=str, required=False, help="Comments on the restaurant")

    def get(self, restaurant_id=None):
        if restaurant_id:
            # Find the restaurant by its ID
            restaurant = next((r for r in restaurants if r["id"] == restaurant_id), None)
            if restaurant:
                return restaurant["reviews"], 200
            return {"message": "Restaurant not fount"}, 404
    
    def post(self, restaurant_id):
        args = ReviewResource.parser.parse_args()
        restaurant = next((r for r in restaurants if r["id"] == restaurant_id), None)
        if not restaurant:
            return {"message": "Restaurant not found."}, 404
        
        if restaurant["reviews"]:
            review_id = max(r["id"] for r in restaurant["reviews"]) + 1
        else:
            review_id = 1
        
        new_review = {"id": review_id, "rating": args["rating"], "comment": args["comment"]}
        restaurant["reviews"].append(new_review)
        return new_review, 201
    
    def put(self, restaurant_id, review_id):
        args = ReviewResource.parser.parse_args()
        restaurant = next((r for r in restaurants if r["id"] == restaurant_id), None)

        if not restaurant:
            return {"message": "Restaurant not found."}, 404
        
        review = next((r for r in restaurant["reviews"] if r["id"] == review_id), None)
        if review:
            if args["rating"] is not None:
                review["rating"] = args["rating"]
            if args["comment"] is not None:
                review["comment"] = args["comment"]
            return review, 200
        else:
            return {"message": "Review not found."}, 404
    
    def delete(self, restaurant_id, review_id):
        restaurant = next((r for r in restaurants if r["id"] == restaurant_id), None)
        if not restaurant:
            return {"message": "Restaurant not found."}, 404

        for i, review in enumerate(restaurant["reviews"]):
            if review["id"] == review_id:
                del restaurant["reviews"][i]
                return "", 200
        return {"message": "Review not found."}, 404
