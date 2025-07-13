from flask import Flask
from flask_restful import Api
from restaurants.api.restaurant_resource import RestaurantResource

# Initialise the Flask app
app = Flask(__name__)
api = Api(app) # wraps the app with the flask_restful Api class

api.add_resource(RestaurantResource, "/restaurants")

@app.route("/")
def hello():
    return {"data": "Hello, Flask!"}

if __name__ == "__main__":
    app.run(debug=True)