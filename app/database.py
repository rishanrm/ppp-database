#!/usr/bin/env python

import re
import subprocess
import csv
import json

import time
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import quote_ident
from google.cloud import storage
from flask import current_app


from psycopg2.extras import RealDictCursor


#from config import Config
from app.config import Config

"""Functionality for connecting to and storing data in a database"""
class DatabaseConnection():

    def __init__(self, database_location='local', database_name='postgres', table_name='postgres'):
        if database_location.lower() == 'local':
            user = Config.POSTGRES_USER_FOR_LOCAL
            password = Config.POSTGRES_PASSWORD_FOR_LOCAL
            port = Config.POSTGRES_PORT_FOR_LOCAL

        elif database_location.lower() == 'cloud':
            user = Config.POSTGRES_USER_FOR_CLOUD
            password = Config.POSTGRES_PASSWORD_FOR_CLOUD
            port = Config.POSTGRES_PORT_FOR_CLOUD
        
        try:
            self.my_connection = psycopg2.connect(
                host=Config.POSTGRES_HOST,
                database=database_name,
                user=user,
                password=password,
                port=port
            )
            self.my_cursor = self.my_connection.cursor()
            self.database_name = database_name
            self.table_name = table_name
            self.file_name = Config.SOURCE_FILE_NAME
            print("\nNew database connection active.")
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            quit("Exiting program.")

    def close_connection(self):
        self.my_connection.commit()
        self.my_cursor.close()
        self.my_connection.close()
        print("Database connection closed.")

    def check_data_present_in_table(self):
        sql_query = f"SELECT exists(\
	                    SELECT  *\
                        FROM    {self.table_name}\
                        LIMIT   1);"
        self.my_cursor.execute(sql_query)
        data_present = self.my_cursor.fetchone()[0]
        return data_present

    def import_csv_data_to_db(self):
        sql_query = f"  COPY      {self.table_name}\
                        FROM      STDIN\
                        DELIMITER ','\
                        CSV       HEADER;"

        with open(self.file_name,  'rb') as csv_file:
            self.my_cursor.copy_expert(sql_query, csv_file)
        self.my_connection.commit()
        print(f"Data uploaded from {self.file_name} to {self.table_name}.")

    def delete_data(self):
        self.my_cursor.execute(f'TRUNCATE {self.table_name}')
        self.my_connection.commit()
        print("The data has been deleted but the table still exists.")
    
    def delete_table(self):
        self.my_cursor.execute(f'DROP TABLE {self.table_name}')
        self.my_connection.commit()
        print("The table has been deleted.")

    """Deprecated method for auto-creating tables in PostgreSQL"""
    @staticmethod
    def create_table_from_csv(db_name, db_url, table_name, file_url):

        subprocess.run([db_name,
                        "--db",
                        db_url,
                        f"{table_name}",
                        f"{file_url}"])

    def store_data(self, status): #Data saving needs to be customized
        # Get retweet count and tweet text regardless of RT status and length
        if hasattr(status, "retweeted_status"):
            retweet_count = status.retweeted_status.retweet_count
            try:
                text = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                text = status.retweeted_status.text
        else:
            retweet_count = status.retweet_count
            try:
                text = status.extended_tweet["full_text"]
            except AttributeError:
                text = status.text

        tweet_analyzer = TweetAnalyzer()
        sentiment = tweet_analyzer.analyze_sentiment(text)

        print(f"{status.id}\
                {status.created_at}\
                {status.user.screen_name}\
                {text}\
                {retweet_count}\
            {sentiment}")

        self.my_cursor.execute(
            "insert into %s values (%%s, %%s, %%s, %%s, %%s, %%s)"\
                % quote_ident(table_name, self.my_cursor),
            [status.id, status.created_at, status.user.screen_name, text,
                retweet_count, sentiment])
        self.my_connection.commit()

    def fetch_most_recent(self, limit=5):
        """Reads the most recent entry of the tweet database
        Args:
            self
            limit: Number of entries to retrieve in reverse chronological order
                   Default: 1
        Returns:
            results: List of results
        """

        self.my_cursor.execute(
            "SELECT *\
            FROM %s\
           LIMIT %%s"
             % quote_ident(self.table_name, self.my_cursor),
            [limit])
        results = self.my_cursor.fetchall()

        for result in results:
            print("")
            for item in result:
                print(item)

        return results

    # def fetch_total_count(self):
    #     stmt = sql.SQL("""            
    #         SELECT row_to_json(t)
    #         FROM (
    #             SELECT COUNT(*) as total
    #             FROM {table_name}
    #         ) t;
    #     """).format(
    #         table_name = sql.Identifier(self.table_name)
    #     )

    #     self.my_cursor.execute(stmt)
    #     results = self.my_cursor.fetchall()
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
        return results

    def fetch_from_db(self, search_term, sort_column, sort_order, offset, limit):

        #Inputs
#        limit = 5
        sort_desc = True
        sort_by_column = 'ad_requests'
        search_column = 'dfp_ad_units'

        data = ()

        #Base query
        stmt = sql.SQL("""
        SELECT array_agg(row_to_json(t))
        FROM (
            SELECT *
            FROM {table_name}
        """).format(
            table_name = sql.Identifier(self.table_name)
        )

        #Filter
        if search_term:
            stmt += sql.SQL("WHERE {search_column} LIKE {search_term} ").format(
                search_column = sql.Identifier(search_column),
                search_term = sql.Literal(search_term + '%%')
                )

        #Sort
        if sort_column:
            stmt += sql.SQL("ORDER BY {sort_column} {sort_order} ").format(
                sort_column = sql.Identifier(sort_column),
                sort_order = sql.SQL(sort_order)
                )

        #Offset
        stmt += sql.SQL("OFFSET %s ")
        data +=(offset,)

        #Limit
        if limit:
            stmt += sql.SQL("LIMIT %s ")
            data += (limit,)

        stmt += sql.SQL(") t;")

        self.my_cursor.execute(stmt, data)
        results = self.my_cursor.fetchall()
        return results

    @staticmethod
    def get_filtered_results_count(results_data):
        if results_data[0][0]:
            return len(results_data[0][0])
        else:
            return 0

    @staticmethod
    def get_json_component(results, data_type):

        if data_type == "total":
            chars_to_strip = 3
        elif data_type == "data":
            chars_to_strip = 2
        results_str = json.dumps(results)[chars_to_strip:-chars_to_strip]
        if results_str == "null":
            results_str = "[]"

        if data_type == "data":
            results_str = "\"rows\": " + results_str

        return results_str

    @staticmethod
    def build_table_json(results_len, total_count_str, results_str):

        results_len_str = "\"total\": " + str(results_len)
        table_json_str = "{ " + results_len_str + ", " + total_count_str + ", " + results_str + " }"
        return table_json_str


class DatabaseInitialization():


    @staticmethod
    def initialize_database(db_location='local', db_name=Config.DB_NAME,\
                            table_name=Config.TABLE_NAME):

        print("Checking for the database...")
        DatabaseInitialization.check_database(db_location, db_name)
        print("Database check complete.")

        print("\nChecking for the data table...")
        DatabaseInitialization.check_table(db_location, db_name, table_name)
        print("Data table check complete.")

        print("\nChecking the data...")
        DatabaseInitialization.check_data(db_location, db_name, table_name)
        print("Data check complete.")
        
        print("\nData is in the database and ready to go.")

    @staticmethod
    def get_user_delete_decision(name):

        print(f"ARE YOU SURE YOU WANT TO DELETE {name}?")
        user_input = input("TYPE 'YES' TO DELETE: ")
        if user_input == "YES":
            return True
        else:
            return False

    @staticmethod
    def check_database(db_location, db_name):

        db = DatabaseConnection(db_location)

        # Change autocommit settings to allow for database creation
        original_autocommit_state = db.my_connection.autocommit
        db.my_connection.autocommit = True

        db_exists = DatabaseInitialization.check_db_exists(db, db_name)
        if db_exists:
            if Config.RESET_DB:
                user_wants_to_delete = DatabaseInitialization.get_user_delete_decision(db_name)
                if user_wants_to_delete:
                    DatabaseInitialization.delete_database(db, db_name)
                    print("Existing database was deleted.")
                    DatabaseInitialization.create_db(db, db_name)
                else:
                    print(f"Database {db_name} was NOT deleted.")
            else:
                print(f"Database {db_name} already exists.")
        else:
            print(f"Database {db_name} does not exist.")
            DatabaseInitialization.create_db(db, db_name)

        db.my_connection.autocommit = original_autocommit_state
        db.close_connection()

    @staticmethod
    def check_db_exists(db, db_name):

        # Select all database names available
        db.my_cursor.execute("SELECT datname FROM pg_database;")
        database_list = db.my_cursor.fetchall()
        db_exists = (db_name,) in database_list
        return db_exists

    @staticmethod
    def delete_database(db, db_name):

        db.my_cursor.execute(f"\
            SELECT pg_terminate_backend(pg_stat_activity.pid)\
            FROM   pg_stat_activity\
            WHERE  pg_stat_activity.datname = '{db_name}'\
            AND    pid <> pg_backend_pid();")
        db.my_connection.set_isolation_level(0)
        db.my_cursor.execute("DROP DATABASE %s;" % quote_ident(
            db_name, db.my_cursor))
        print("Database deleted.")

    @staticmethod
    def create_db(db, db_name):

        db_sql_query = (f"CREATE DATABASE {db_name};")
        db.my_cursor.execute(db_sql_query)
        print(f'Database {db_name} created.')

    @staticmethod
    def check_table(db_location, db_name, table_name):

        db = DatabaseConnection(db_location, database_name=db_name)

        # Change autocommit settings to allow for database creation
        original_autocommit_state = db.my_connection.autocommit
        db.my_connection.autocommit = True

        table_exists = DatabaseInitialization\
            .check_table_exists(db, table_name)
        if table_exists:
            if Config.RESET_TABLE:
                user_wants_to_delete = DatabaseInitialization\
                    .get_user_delete_decision(table_name)
                if user_wants_to_delete:
                    DatabaseInitialization.delete_table(\
                        db, table_name, original_autocommit_state)
                    print("Existing table was deleted.")
                    DatabaseInitialization.create_table(db, table_name)
                else:
                    print(f"Table {table_name} was NOT deleted.")
            else:
                print(f"Table {table_name} already exists.")
        else:
            print(f"Table {table_name} does not exist.")
            DatabaseInitialization.create_table(db, table_name)

        db.my_connection.autocommit = original_autocommit_state
        db.close_connection()

    @staticmethod
    def check_table_exists(db, table_name):

        check_table_exists_sql_query = (f"""
            SELECT EXISTS (
                SELECT FROM pg_tables
                WHERE       tablename  = '{table_name}');""")
        db.my_cursor.execute(check_table_exists_sql_query)
        table_exists = db.my_cursor.fetchone()[0]
        return table_exists

    def delete_table(db, table_name, original_autocommit_state):
        db.my_cursor.execute("DROP TABLE %s;" % quote_ident(
            table_name, db.my_cursor))
        print("Table deleted.")

    @staticmethod
    def ensure_data_table_exists(db_name, table_name):
        # Connect to the default postgres database
        db = DatabaseConnection(db_location, database_name=db_name)

        # Change autocommit settings to allow for database creation
        original_autocommit_state = db.my_connection.autocommit
        db.my_connection.autocommit = True

        table_exists = DatabaseInitialization.check_table_exists(db, table_name)
        if not table_exists:
            print('The table named "%s" does not exist. Creating it now...'\
            % table_name)
            DatabaseInitialization.create_table(db, table_name)
        else:
            print('The table named "%s" already exists.' % table_name)


        # Reset settings (not required) and close connection
        db.my_connection.autocommit = original_autocommit_state
        db.close_connection()

    @staticmethod
    def create_table(db, table_name):

        table_sql_query = DatabaseInitialization\
            .create_table_sql_query_string(table_name)
        db.my_cursor.execute(table_sql_query)
        print(f"Table {table_name} was created.")

    @staticmethod
    def create_table_sql_query_string(table_name):

        if Config.MANUALLY_CREATE_TABLE:
            print("SQL query is being manually configured in the python code.")
            create_table_sql_query = ("""
                CREATE TABLE IF NOT EXISTS {table_name}(
                    PRIMARY KEY(tweet_id),
                    tweet_id	    BIGINT			,
                    created_at	    TIMESTAMP		,
                    screen_name	    TEXT			,
                    full_text	    TEXT			,
                    retweet_count   INTEGER         ,
                    sentiment	    NUMERIC(7, 3));"""\
                .format(table_name=table_name))
        else:
            csv_headers = HeaderNames.get_csv_column_headers(
                Config.SOURCE_FILE_NAME)
            sql_column_names = HeaderNames.format_sql_column_names(csv_headers)
            create_table_sql_query =\
                f"CREATE TABLE IF NOT EXISTS {table_name}(\n"
            for i in range(len(sql_column_names)):
                if i < len(sql_column_names)-1:
                    create_table_sql_query += "\t"\
                        + sql_column_names[i]\
                        + " varchar(255),\n"
                else:
                    create_table_sql_query += "\t"\
                        + sql_column_names[i]\
                        + " varchar(255)"
            create_table_sql_query += ");"
        return create_table_sql_query

    @staticmethod
    def check_data(db_location, db_name, table_name):

        db = DatabaseConnection(db_location, database_name=db_name, table_name = table_name)

        # Change autocommit settings to allow for database creation
        original_autocommit_state = db.my_connection.autocommit
        db.my_connection.autocommit = True

        data_exists = db.check_data_present_in_table()
        if data_exists:
            if Config.RESET_DATA:
                user_wants_to_delete = DatabaseInitialization\
                    .get_user_delete_decision(f"data in {db.table_name}")
                if user_wants_to_delete:
                    db.delete_data()
                    db.import_csv_data_to_db()
                    print("Data has been overwritten in the database.")
                else:
                    print("Existing data was NOT overwritten.")
            else:
                print(f"Table {table_name} already has data in it.")
        else:
            db.import_csv_data_to_db()
            print("Data uploaded from file to database.")

        db.my_connection.autocommit = original_autocommit_state
        db.close_connection()

"""Functionality for initial data population in a database"""
class HeaderNames():

    @staticmethod
    def get_csv_column_headers(source_file_name=Config.SOURCE_FILE_NAME):

        with open(source_file_name, 'r', encoding='utf-8-sig') as f:
            d_reader = csv.DictReader(f)
            headers = d_reader.fieldnames
            return headers

    @staticmethod
    def format_sql_column_names(headers):

        headers = [' '.join(re.sub( \
            "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", \
            header).split()).replace(" ", "_").lower()\
            for header in headers]
        return headers
    
    @staticmethod
    def get_sql_names_from_file(source_file_name=Config.SOURCE_FILE_NAME):

        headers = get_csv_column_headers(source_file_name)
        sql_columns = format_sql_column_names(headers)
        return sql_columns


"""
#p355491811298-swj734@gcp-sa-cloud-sql.iam.gserviceaccount.com
355491811298-compute@developer.gserviceaccount.com
gcloud sql connect ppp-test-16 --user=root
gcloud sql connect ppp-test-16 --user=postgres < employees.sql
https://us-central1-ppp-test-283923.cloudfunctions.net/codelab-sql
https://us-central1-ppp-test-283923.cloudfunctions.net/function-1
"""