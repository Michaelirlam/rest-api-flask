from flask import Flask, Blueprint, jsonify
from flask_restful import Api
from restaurants.api.restaurant_resource import RestaurantResource
from restaurants.api.review_resource import ReviewResource
from restaurants.db import init_db, init_ma


# Initialise the Flask app
app = Flask(__name__)
api = Api(app) # wraps the app with the flask_restful Api class

app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///restaurants.db")
db = init_db(app)
ma = init_ma(app)

# Creates blueprint for version 1 of the REST API 
v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api_v1 = Api(v1_bp)

# Version 2 for future use
v2_bp = Blueprint("api_v2", __name__, url_prefix="/api/v2")
api_v2 = Api(v2_bp)

app.register_blueprint(v1_bp)
app.register_blueprint(v2_bp)

api.add_resource(RestaurantResource, "/restaurants", "/restaurants/<int:restaurant_id>")
api.add_resource(ReviewResource, "/restaurants/<int:restaurant_id>/reviews", "/restaurants/<int:restaurant_id>/reviews/<int:review_id>")

api_v1.add_resource(RestaurantResource, "/restaurants", "/restaurants/<int:restaurant_id>")
api_v1.add_resource(ReviewResource, "/restaurants/<int:restaurant_id>/reviews", "/restaurants/<int:restaurant_id>/reviews/<int:review_id>")

@app.route("/")
def hello():
    return {"data": "Hello, Flask!"}

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({
        "error": "InternalServerError",
        "message": "An unexpected error occured."
    }), 500

if __name__ == "__main__":
    app.run(debug=True)