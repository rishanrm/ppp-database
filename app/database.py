#!/usr/bin/env python

# import os
import re
import subprocess
import csv
import json

# import time
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import quote_ident
# from google.cloud import storage
from flask import current_app
from collections import OrderedDict

from psycopg2.sql import NULL


# from psycopg2.extras import RealDictCursor


#from config import Config
from config import Config

"""Functionality for connecting to and storing data in a database"""
class DatabaseConnection():

    def __init__(self, database_location='local', database_name='postgres', table_name='postgres'):

        user = current_app.config["POSTGRES_USER"]
        password = current_app.config["POSTGRES_PASSWORD"]
        port = current_app.config["POSTGRES_PORT"]
        try:
            self.my_connection = psycopg2.connect(
                host=current_app.config["POSTGRES_HOST"],
                database=database_name,
                user=user,
                password=password,
                port=port
            )
            self.my_cursor = self.my_connection.cursor()
            self.database_name = database_name
            self.table_name = table_name
            print("\nNew database connection active.")
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            quit("Exiting program.")

    # def close_connection(self):
    #     self.my_connection.commit()
    #     self.my_cursor.close()
    #     self.my_connection.close()
    #     print("Database connection closed.")

    # def check_data_present_in_table(self):
    #     sql_query = f"SELECT exists(\
	#                     SELECT  *\
    #                     FROM    {self.table_name}\
    #                     LIMIT   1);"
    #     self.my_cursor.execute(sql_query)
    #     data_present = self.my_cursor.fetchone()[0]
    #     return data_present

    # def import_csv_data_to_db(self):
    #     sql_query = f"  COPY      {self.table_name}\
    #                     FROM      STDIN\
    #                     DELIMITER ','\
    #                     CSV       HEADER;"

    #     with open(self.file_name,  'rb') as csv_file:
    #         self.my_cursor.copy_expert(sql_query, csv_file)
    #     self.my_connection.commit()
    #     print(f"Data uploaded from {self.file_name} to {self.table_name}.")

    # def delete_data(self):
    #     self.my_cursor.execute(f'TRUNCATE {self.table_name}')
    #     self.my_connection.commit()
    #     print("The data has been deleted but the table still exists.")
    
    # def delete_table(self):
    #     self.my_cursor.execute(f'DROP TABLE {self.table_name}')
    #     self.my_connection.commit()
    #     print("The table has been deleted.")

    # """Deprecated method for auto-creating tables in PostgreSQL"""
    # @staticmethod
    # def create_table_from_csv(db_name, db_url, table_name, file_url):

    #     subprocess.run([db_name,
    #                     "--db",
    #                     db_url,
    #                     f"{table_name}",
    #                     f"{file_url}"])

    # def store_data(self, status): #Data saving needs to be customized
    #     # Get retweet count and tweet text regardless of RT status and length
    #     if hasattr(status, "retweeted_status"):
    #         retweet_count = status.retweeted_status.retweet_count
    #         try:
    #             text = status.retweeted_status.extended_tweet["full_text"]
    #         except AttributeError:
    #             text = status.retweeted_status.text
    #     else:
    #         retweet_count = status.retweet_count
    #         try:
    #             text = status.extended_tweet["full_text"]
    #         except AttributeError:
    #             text = status.text

    #     tweet_analyzer = TweetAnalyzer()
    #     sentiment = tweet_analyzer.analyze_sentiment(text)

    #     print(f"{status.id}\
    #             {status.created_at}\
    #             {status.user.screen_name}\
    #             {text}\
    #             {retweet_count}\
    #         {sentiment}")

    #     self.my_cursor.execute(
    #         "insert into %s values (%%s, %%s, %%s, %%s, %%s, %%s)"\
    #             % quote_ident(table_name, self.my_cursor),
    #         [status.id, status.created_at, status.user.screen_name, text,
    #             retweet_count, sentiment])
    #     self.my_connection.commit()

    # def fetch_most_recent(self, limit=5):
    #     """Reads the most recent entry of the tweet database
    #     Args:
    #         self
    #         limit: Number of entries to retrieve in reverse chronological order
    #                Default: 1
    #     Returns:
    #         results: List of results
    #     """

    #     self.my_cursor.execute(
    #         "SELECT *\
    #         FROM %s\
    #        LIMIT %%s"
    #          % quote_ident(self.table_name, self.my_cursor),
    #         [limit])
    #     results = self.my_cursor.fetchall()

    #     for result in results:
    #         print("")
    #         for item in result:
    #             print(item)

    #     return results

    def fetch_total_count(self):

        stmt = sql.SQL("""            
            SELECT row_to_json(t)
            FROM (
                SELECT COUNT(*) as "totalNotFiltered"
                FROM {table_name}
            ) t;
        """).format(
            table_name = sql.Identifier(self.table_name)
        )

        self.my_cursor.execute(stmt)
        results = self.my_cursor.fetchall()
        print("TOTAL FETCH COUNT:")
        print(results)
        return results

    def run_sql_query(self, args, query_features, return_type):
        sql_query_data = self.build_query(args, query_features)
        return self.fetch_from_db(sql_query_data, return_type)

    def build_query(self, args, query_features):
        query_start = self.get_query_start()
        query_body = self.get_query_body(args, query_features)
        query_end = self.get_query_end()
        
        return {
            "query": query_start + query_body["query"] + query_end,
            "data": query_body["data"]
        }

    def get_query_start(self):
        return sql.SQL("""
        SELECT array_agg(row_to_json(t))
        FROM (
            SELECT *
            FROM {table_name}
            WHERE ''=''
        """).format(
            table_name = sql.Identifier(self.table_name)
        )

    def get_query_body(self, args, query_features):
        # print("ARGS:")
        # print(args)
        # print("QUERY FEATURES:")
        # print(query_features)
        # print("URL GIVEN:")
        # print(args["page"])
        query_body = sql.SQL("")
        data = ()
        
        args_order = ["page", "search", "filter", "sort", "order", "offset", "limit"]
        args_dict = OrderedDict((arg, args.get(arg)) for arg in args_order)

        print("\n")
        print("ARGS DICT:")
        print(args_dict)
        print("\n")

        if(args_dict["filter"] == None):
            args_dict["filter"] = {"state": None}
        else:
            args_dict["filter"] = json.loads(args_dict["filter"])
            if "state" not in args_dict["filter"]:
                args_dict["filter"]["state"] = None
        print("\nARGS DICT, is there a filter?")
        print(args_dict)
        print("filter" in args_dict)
        print("DID THAT SAY TRUE?")
        # print("ARGS:")
        # print(args)

        # print(args_dict.keys)
        for arg in args_dict:
            print("ARG:")
            print(arg)
            if (arg == "filter"):
                print(arg)
                print(args_dict[arg])
                print("THAT WAS THE FILTER")
            if args_dict[arg] != "" and args_dict[arg] != "undefined" and args_dict[arg] != None and arg in query_features:
                if arg == "search":
                    # print(args_dict["search"])
                    # print(args_dict["page"])
                    query_body += self.sql_field_search(args_dict["page"], args_dict["search"])
                if arg == "filter":
                    print("THERE'S A FILTER\n\n\n\n\n\n")
                    # print(filter_data)
                    query_body += self.sql_field_filter(args_dict["filter"])
                if arg == "sort":
                    query_body += self.sql_field_sort(args_dict["sort"], args_dict["order"])
                if arg == "offset":
                    offset_results = self.sql_field_offset(args_dict["offset"])
                    query_body += offset_results["sql"]
                    data += offset_results["data"]
                if arg == "limit":
                    limit_results = self.sql_field_limit(args_dict["limit"])
                    query_body += limit_results["sql"]
                    data += limit_results["data"]
        return {
            "query": query_body,
            "data": data
        }

    @staticmethod
    def sql_field_search(page, search_term):
        search_sql = sql.SQL('AND (')
        search_term_count = 0
        if page == "data-150k-and-up":
            column_headers = current_app.config["HEADERS_150K_AND_UP"]
        elif page == "data-under-150k":
            column_headers = current_app.config["HEADERS_UNDER_150K"]
        # column_headers = DatabaseNames.get_csv_column_headers(current_app.config.SOURCE_FILE_NAME)
        numeric_headers = current_app.config["NUMERIC_HEADERS"]
        string_headers = [column for column in column_headers if column not in numeric_headers]

        for header in string_headers:
            if search_term_count == 0:
                prefix=""
            else:
                prefix = "OR"
            search_sql += sql.SQL("{prefix} LOWER({search_column}) LIKE LOWER({search_term}) ").format(
                prefix = sql.SQL(prefix),
                search_column = sql.Identifier(header),
                search_term=sql.Literal('%%' + search_term + '%%')
            )
            search_term_count += 1

        for header in numeric_headers:
            if header in column_headers:
                #Loan Amount search
                search_term = search_term.strip("$").replace(',', '').split(".", 1)[0]
                if search_term.isdigit():
                    search_sql += sql.SQL("OR {search_column} = {search_term} ").format(
                        search_column = sql.Identifier(header),
                        search_term = sql.Literal(search_term)
                    )

        search_sql += sql.SQL(') ')
        print (search_sql)
        return search_sql

    @staticmethod
    def sql_field_filter(filter_data):
        print("FILTER DATA:\n\n\n\n\n\n")
        print(filter_data)
        filter_sql = sql.SQL("")
        # filter_data = json.loads(filter_data)
        numeric_headers = current_app.config["NUMERIC_HEADERS"]
        for filter in filter_data:
            print("FILTER:")
            print(filter)
            print("END FILTER\n\n\n\n")
            if filter not in numeric_headers:

                if (filter == "address" or filter == "city") and (filter_data[filter].replace('/', '').lower() == "na"):
                    equality_type = "LIKE"
                    modifier_opening = "LOWER("
                    filter_term = sql.Literal("N/A")
                    modifier_closing = ")"
                elif filter =="state" and filter_data[filter] == None:
                    equality_type = "IS"
                    modifier_opening = ""
                    filter_term = sql.Literal(filter_data[filter])
                    modifier_closing = ""
                elif (filter == "zip" or filter == "naicscode") and (filter_data[filter].replace('/', '').lower() == "na"):
                    equality_type = "IS"
                    modifier_opening = ""
                    filter_term = sql.Literal(None)
                    modifier_closing = ""
                else:
                    equality_type = "LIKE"
                    modifier_opening = "LOWER("
                    filter_term = sql.Literal(filter_data[filter] + '%%')
                    modifier_closing = ")"

                filter_sql += sql.SQL("AND LOWER({filter_column}) {equality_type} {modifier_opening}{filter_term}{modifier_closing} ").format(
                    filter_column = sql.Identifier(filter),
                    modifier_opening = sql.SQL(modifier_opening),
                    equality_type = sql.SQL(equality_type),
                    filter_term = filter_term,
                    modifier_closing = sql.SQL(modifier_closing)
                )
            elif filter in numeric_headers:
                equality_type = "="
                modifier_opening = ""
                filter_term = filter_data[filter].strip("$").replace(',', '')
                modifier_closing = ""
                if not filter_term.replace('.', '').isdigit():
                    if filter_term.replace('/', '').lower() == "na":
                        equality_type = "IS"
                        filter_term = None
                    else:
                        filter_term = "999999999" # Will search for this hardcoded num which should not return results
                
                filter_sql += sql.SQL("AND {filter_column} {equality_type} {filter_term} ").format(
                    filter_column = sql.Identifier(filter),
                    equality_type = sql.SQL(equality_type),
                    filter_term = sql.Literal(filter_term)
                )
                # filter_term = filter_data[filter].strip("$").replace(',', '').split(".", 1)[0]
                # if filter_term.isdigit():
                #     filter_sql += sql.SQL("AND {filter_column} = {filter_term} ").format(
                #         filter_column = sql.Identifier(filter),
                #         filter_term = sql.Literal(filter_term)
                #     )

        return filter_sql
        
    @staticmethod
    def sql_field_sort(sort_column, sort_order):
        null_position = ""
        if sort_order.lower() == "desc":
            null_position = "LAST"
        elif sort_order.lower() == "asc":
            null_position = "FIRST"
        return sql.SQL("ORDER BY {sort_column} {sort_order} NULLS {null_position} ").format(
            sort_column = sql.Identifier(sort_column),
            sort_order = sql.SQL(sort_order),
            null_position = sql.SQL(null_position)
            )
        
    @staticmethod
    def sql_field_offset(offset):
        return {
            "sql": sql.SQL("OFFSET %s "),
            "data": (offset,)
        }
        
    @staticmethod
    def sql_field_limit(limit):
        return {
            "sql": sql.SQL("LIMIT %s "),
            "data": (limit,)
        }

    @staticmethod
    def get_query_end():
        return sql.SQL(") t;")

    def fetch_from_db(self, sql_query_data, return_type):
        print("SQL QUERY:")
        print(sql_query_data["query"])
        print(sql_query_data["data"])
        self.my_cursor.execute(sql_query_data["query"], sql_query_data["data"])
        results = self.my_cursor.fetchall()

        if return_type == "data":
            return results
        elif return_type == "count":
            if results[0][0]:
                return len(results[0][0])
            else:
                return 0

    @staticmethod
    def get_json_component(results, data_type):

        if data_type == "total":
            chars_to_strip = 3
        elif data_type == "data":
            if (results[0][0]) != None:
                for result in results[0][0]:
                    for key, value in result.items():
                        if key in current_app.config["NAMES_TO_CAPITALIZE"]:
                            result[key] = value.title()
            chars_to_strip = 2
        results_str = json.dumps(results)[chars_to_strip:-chars_to_strip]
        if results_str == "null":
            results_str = "[]"

        if data_type == "data":
            results_str = "\"rows\": " + results_str

        return results_str

    @staticmethod
    def build_table_json(results_len_str, total_count_str, results_str):

        #results_len_str = "\"total\": " + str(results_len)
        table_json_str = "{ " + results_len_str + ", " + total_count_str + ", " + results_str + " }"
        return table_json_str

    def get_column_options(self, column):
        print('IN COLUMN OPTIONS')
        query= sql.SQL("""
            SELECT DISTINCT {column}
            FROM            {table_name}
            """).format(
                column = sql.Identifier(column),
                table_name = sql.Identifier(self.table_name)
            )
        self.my_cursor.execute(query)
        results = self.my_cursor.fetchall()
        return results

    @staticmethod
    def get_column_options_dict(column_options, column=""):
        options_dict = {}
        for option in column_options:
            options_dict[option[0]] = option[0]
        # return (options_dict)
        return ({column: options_dict}) #Returns result labeled by the column name

    def get_all_column_options(self, column_headers):
        query = sql.SQL("""SELECT """)
        i = 0
        for header in column_headers:
            if i == 0:
                prefix = ""
            else:
                prefix = ","
            query += sql.SQL("""
                {prefix} array_agg(DISTINCT {column}) AS {column}""").format(
                    prefix = sql.SQL(prefix),
                    column = sql.SQL(header))
            i += 1
        query += sql.SQL("""
            FROM {table};""".format(table = self.table_name))
        self.my_cursor.execute(query)
        results = self.my_cursor.fetchall()
        return results[0]

    @staticmethod
    def format_column_options_json(column_headers, column_options):
    # Returns a single dictionary with all unique values for all columns
        all_options_dict = {}
        i = 0
        for column in column_options:            
            options_dict = {}
            for option in column:
                options_dict[option] = option
            all_options_dict[column_headers[i]] = options_dict
            i += 1
        return all_options_dict
        

"""Functionality for initial data population in a database"""
class DatabaseNames():

    @staticmethod
    def postgres_name(name):
        return name\
            .split(".")[0]\
            .replace(" ", "_")\
            .replace("-", "")\
            .lower()
        # DB_NAME = name_root + "_db"
        # TABLE_NAME = name_root + "_table"

"""
#p355491811298-swj734@gcp-sa-cloud-sql.iam.gserviceaccount.com
355491811298-compute@developer.gserviceaccount.com
gcloud sql connect ppp-test-16 --user=root
gcloud sql connect ppp-test-16 --user=postgres < employees.sql
https://us-central1-ppp-test-283923.cloudfunctions.net/codelab-sql
https://us-central1-ppp-test-283923.cloudfunctions.net/function-1
"""
