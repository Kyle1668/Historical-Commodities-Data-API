from flask_restful import Resource


class CommoditiesEndpoints(Resource):
    def get(self):
        query_params = {
            "commodity": None,
            "start_date": None,
            "end_date": None
        }
        return {"hello": "world"}

    def post(selfs):
        return {"hello", "post"}
