import json

from flask import current_app

from database import DatabaseConnection

class Data():

    @staticmethod
    def get_data(request):
        if "filter" in request.args:
            if request.args["page"] == "data-under-150k":
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

        if request.args["page"] == "data-under-150k":
            db_name = current_app.config["DB_NAME_ROOT_UNDER_150K"]
            table_name = current_app.config["DB_NAME_ROOT_UNDER_150K"] + "_" + state.lower()
        elif request.args["page"] == "data-150k-and-up":
            db_name = current_app.config["DB_NAME_ROOT_150K_AND_UP"]
            table_name = current_app.config["DB_NAME_ROOT_150K_AND_UP"]

        with current_app.app_context():
            db = DatabaseConnection(db_name, table_name)

        # total_count = db.fetch_total_count()
        # total_count_str = db.get_json_component(total_count, "total")

        print("GETTING FILTERED COUNT STR...")
        # filtered_results_count = db.run_sql_query(
        #     request.args, ["search", "filter"], "count")
        # filtered_count_str = "\"total\": " + str(filtered_results_count)
        # filtered_count_str = "\"total\": " + "555429"

        # filtered_query = db.build_query(request.args, ["search", "filter"])
        filtered_count = db.fetch_filtered_count(request.args, ["search", "filter"])
        filtered_count_str = db.get_json_component(filtered_count, "total")
        print(filtered_count_str)

        print("GOT FILTERED COUNT STR")

        total_count = db.fetch_count(
            request.args, ["search", "filter"], "totalNotFiltered")
        total_count_str = db.get_json_component(total_count, "total")
        print(total_count_str)
        print("GOT TOTAL COUNT STR")

        filtered_count_str = total_count_str.replace("'totalNotFiltered'", "total")

        # filtered_count = db.fetch_count(
        #     request.args, ["search", "filter"], "total")
        # # filtered_count_str = db.get_json_component(filtered_count, "total")
        # print(filtered_count_str)
        # print("GOT FILTERED COUNT STR")
        # # filtered_count_str = total_count_str.replace('NotFiltered', '')

        print("GETTING RESULTS STR...")
        results_data = db.run_sql_query(
            request.args, ["search", "filter", "sort", "offset", "limit"], "data")
        results_str = db.get_json_component(results_data, "data")
        print("GOT RESULTS STR")

        table_data_json = db.build_table_json(
            filtered_count_str, total_count_str, results_str)
        print("GOT TABLE JSON")

        return json.loads(table_data_json)
