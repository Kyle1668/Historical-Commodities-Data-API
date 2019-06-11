from os import environ
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from commodities_endpoints import CommoditiesEndpoints

application = Flask(__name__)
api = Api(application)

api.add_resource(CommoditiesEndpoints, '/commodity')

if __name__ == "__main__":
    if "ENV" not in environ or environ["ENV"] == "development":
        print("Loading ENV VARS from .env")
        load_dotenv()

    application.run(host='0.0.0.0', port=8080)
