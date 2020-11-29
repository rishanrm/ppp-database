import json

from flask import current_app

from app.config import Config
from app.database import DatabaseConnection

class Data():

    @staticmethod
    def get_data(request):
        state = ""
        db_name = ""
        table_name = ""

        if "filter" in request.args:
            print(request.args["filter"])
            substr = 'state":"'
            state_index = request.args["filter"].index(substr)+len(substr)
            state = request.args["filter"][state_index:state_index+2]
        else:
            print("NO STATE")
            state = "unstated"

        print(request.args["page"])
        # sub_url = request.args["page"]
        if request.args["page"] == "data-under-150k":
            db_name = Config.DB_NAME_ROOT_UNDER_150K
            table_name = Config.DB_NAME_ROOT_UNDER_150K + "_" + state.lower()
        elif request.args["page"] == "data-150k-and-up":
            db_name = Config.DB_NAME_ROOT_150K_AND_UP
            table_name = Config.DB_NAME_ROOT_150K_AND_UP
        # print(db_name)
        # print(table_name)

        print("REQUEST START:")
        print(request.args)
        print("REQUEST END")

        with current_app.app_context():
            db = DatabaseConnection("local", db_name, table_name)
            # db = DatabaseConnection("local", Config.DB_NAME, Config.TABLE_NAME)
    #        db = DatabaseInitialization.initialize_database("local")

        total_count = db.fetch_total_count()
        total_count_str = db.get_json_component(total_count, "total")

        filtered_results_count = db.run_sql_query(
            request.args, ["search", "filter"], "count")
        filtered_count_str = "\"total\": " + str(filtered_results_count)

        results_data = db.run_sql_query(
            request.args, ["search", "filter", "sort", "offset", "limit"], "data")
        results_str = db.get_json_component(results_data, "data")

        table_data_json = db.build_table_json(
            filtered_count_str, total_count_str, results_str)
        print(type(table_data_json))

        print("PARAMS ROUTE")
        print(type(json.loads(table_data_json)))

        return json.loads(table_data_json)
