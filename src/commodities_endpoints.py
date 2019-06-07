from flask_restful import Resource


class CommoditiesEndpoints(Resource):
    def get(self):
        return {'hello': 'world'}
