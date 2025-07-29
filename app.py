from flask import Flask
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

api.add_resource(RestaurantResource, "/restaurants", "/restaurants/<int:restaurant_id>")
api.add_resource(ReviewResource, "/restaurants/<int:restaurant_id>/reviews", "/restaurants/<int:restaurant_id>/reviews/<int:review_id>")

@app.route("/")
def hello():
    return {"data": "Hello, Flask!"}

if __name__ == "__main__":
    app.run(debug=True)