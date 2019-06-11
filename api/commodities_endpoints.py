import numpy as np
from psycopg2 import Error
from flask import jsonify
from flask_restful import Resource
from database import postgres_connection
from flask import request, make_response


class CommoditiesEndpoints(Resource):

    def get(self):
        if request.args.get("start_date") is None or request.args.get("end_date") is None:
            return self.missing_query_param_response()
        elif request.args.get("commodity_type") not in ["gold", "silver"]:
            return self.incorrect_commodity_type_response(request.args.get("commodity_type"))

        data = self.get_time_series_data(
            postgres_connection,
            request.args.get("start_date"),
            request.args.get("end_date"),
            request.args.get("commodity_type"),
        )

        return self.success_result(data)

    def success_result(self, time_series_data):
        data_result = None
        mean_result = None
        variance_result = None

        if time_series_data:
            data_result = [{str(data[0]): data[1]} for data in time_series_data]
            prices_list = [data[1] for data in time_series_data]
            mean_result = np.mean(prices_list)
            variance_result = np.var(prices_list)

        return jsonify({
            "data": data_result,
            "mean": mean_result,
            "variance": variance_result
        })

    def missing_query_param_response(self):
        json = jsonify({"error": True, "message": "Incorrect or missing query parameters"})
        return make_response(json, 400)

    def incorrect_commodity_type_response(self, wrong_commodity):
        missing_message = "Missing query parameter commodity (gold/silver)"
        incorrect_message = "Incorrect commodity type (not gold or silver)"
        json = jsonify({
            "error": True,
            "message": incorrect_message if wrong_commodity else missing_message
        })
        return make_response(json, 400)

    def get_time_series_data(self, pg_db_connection, start_date, end_date, commodity):
        cursor = pg_db_connection.cursor()
        query = """
        SELECT * FROM %s 
        WHERE date >= '%s' 
          AND date <= '%s';
        """ % (commodity, start_date, end_date)

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            if result:
                return result
            else:
                return None
        except Error:
            print("ERROR IN SELECT")
            pass

        pg_db_connection.commit()
        cursor.close()
