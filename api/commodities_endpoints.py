from psycopg2 import Error
from flask import jsonify
from flask_restful import Resource
from database import postgres_connection


class CommoditiesEndpoints(Resource):
    def get(self):
        data = self.get_time_series_data(postgres_connection, "2019-06-03", "2019-06-11", "gold")

        return self.success_result(data)

    def success_result(self, time_series_data):
        return jsonify({
            "data": [{str(data[0]): data[1]} for data in time_series_data],
            "mean": "",
            "variance": ""
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
            return cursor.fetchall()
        except Error:
            print("ERROR IN SELECT")
            pass

        pg_db_connection.commit()
        cursor.close()
