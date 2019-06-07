from flask import Flask
from flask_restful import Api

from src.commodities_endpoints import CommoditiesEndpoints

application = Flask(__name__)
api = Api(application)

api.add_resource(CommoditiesEndpoints, '/commodity')

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8080)
