from psycopg2 import Error
from flask import jsonify
from flask_restful import Resource, reqparse
from database import postgres_connection
from flask import request, make_response


class CommoditiesEndpoints(Resource):

    def get(self):
        print(request.args)
        data = self.get_time_series_data(
            postgres_connection,
            request.args.get("start_date"),
            request.args.get("end_date"),
            request.args.get("commodity_type"),
        )

        return self.success_result(data)

    def success_result(self, time_series_data):
        data_result = None
        mean_reuslt = None
        variance_reuslt = None

        if time_series_data:
            data_result = [{str(data[0]): data[1]} for data in time_series_data]

        return jsonify({
            "data": data_result,
            "mean": mean_reuslt,
            "variance": variance_reuslt
        })

    def calculate_mean(self, query_results):
        pass

    def missing_query_param_response(self, parameters):
        pass

    def incorrect_commodity_type_response(self, wrong_commodity):
        pass

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
