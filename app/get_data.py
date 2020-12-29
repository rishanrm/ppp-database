import json

from flask import current_app

from database import DatabaseConnection

class Data():

    @staticmethod
    def get_data(request):
        if "filter" in request.args:
            if ((request.args["page"] == "data-under-150k") or (request.args["page"] == "all-data")):
                substr = 'state":"'
                if substr in request.args["filter"]:
                    state_index = request.args["filter"].index(substr)+len(substr)
                    state = request.args["filter"][state_index:state_index+2]
                else:
                    state = "unstated"
            elif request.args["page"] == "data-150k-and-up":
                state = "unstated"
        else:
            state = "unstated"

        if request.args["page"] == "all-data":
            db_name = current_app.config["DB_NAME_ROOT_ALL_DATA"]
            table_name = current_app.config["DB_NAME_ROOT_ALL_DATA"] + \
                "_" + state.lower()
            print(f"Table name:\n{table_name}")
        elif request.args["page"] == "data-under-150k":
            db_name = current_app.config["DB_NAME_ROOT_UNDER_150K"]
            table_name = current_app.config["DB_NAME_ROOT_UNDER_150K"] + "_" + state.lower()
        elif request.args["page"] == "data-150k-and-up":
            db_name = current_app.config["DB_NAME_ROOT_150K_AND_UP"]
            table_name = current_app.config["DB_NAME_ROOT_150K_AND_UP"]

        with current_app.app_context():
            db = DatabaseConnection(db_name, table_name)

        filtered_count = db.fetch_filtered_count(request.args, ["search", "filter"])
        filtered_count_str = db.get_json_component(filtered_count, "total")

        total_count = db.fetch_total_count()
        total_count_str = db.get_json_component(total_count, "total")

        results_data = db.run_sql_query(
            request.args, ["search", "filter", "sort", "offset", "limit"], "data")
        results_str = db.get_json_component(results_data, "data")

        summary_data = db.fetch_summary_data(
            request.args, ["search", "filter"])
        summary_data_str = db.get_json_component(summary_data, "footer")
        print(summary_data_str)

        table_data_json = db.build_table_json(
            filtered_count_str, total_count_str, results_str, summary_data_str)
            # filtered_count_str, total_count_str, results_str)

        with open('data2.txt', 'w') as outfile:
            json.dump(table_data_json, outfile)

        return json.loads(table_data_json)
