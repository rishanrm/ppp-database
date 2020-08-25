#!/usr/bin/env python

import re
import subprocess
import csv

import time
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import quote_ident
from google.cloud import storage
from flask import current_app


from psycopg2.extras import RealDictCursor


#from config import Config
from app.config import Config

"""Functionality for initializing a database"""
class DatabaseInitialization():

    def reset_database(db_name, reset_db=False):

        if reset_db:
            db = DatabaseConnection()

            # Change autocommit settings to allow for database creation
            original_autocommit_state = db.my_connection.autocommit
            db.my_connection.autocommit = True

            # Select all database names available
            db.my_cursor.execute("SELECT datname FROM pg_database;")
            database_list = db.my_cursor.fetchall()

            if (db_name,) in database_list:
                user_wants_to_delete = DatabaseInitialization.get_user_db_delete_decision()
                if user_wants_to_delete:
                    DatabaseInitialization.delete_database(db, db_name, original_autocommit_state)
                else:
                    print("Database was NOT deleted.")
            else:
                print("You want to reset the DB but it does not already exist.")

    @staticmethod
    def get_user_db_delete_decision():
        print("ARE YOU SURE YOU WANT TO DELETE THE OLD DATABASE?")
        user_input = input("TYPE 'YES' TO DELETE: ")
        if user_input == "YES":
            return True
        else:
            return False

    def delete_database(db, db_name, original_autocommit_state):

#        print(f"\
#            SELECT pg_terminate_backend(pid)\
        #     FROM   pg_stat_activity\
        #     WHERE  datname = {db_name};")
        # quit()
        # db.my_cursor.execute(f"\
        #     SELECT pg_terminate_backend(pid)\
        #     FROM   pg_stat_activity\
        #     WHERE  datname = {db_name};")
        db.my_cursor.execute(f"\
            SELECT pg_terminate_backend(pg_stat_activity.pid)\
            FROM   pg_stat_activity\
            WHERE  pg_stat_activity.datname = '{db_name}'\
            AND    pid <> pg_backend_pid();")
        db.my_connection.set_isolation_level(0)
        db.my_cursor.execute("DROP DATABASE %s;" % quote_ident(
            db_name, db.my_cursor))
        db.my_connection.autocommit = original_autocommit_state
        db.close_connection()
        print("Database deleted.")

    def check_database(db_name):
        """Checks if the database exists, and if not, creates it.
        Args:
            db_name: name of the database
        Returns:
            N/A
        """
        # Connect to the default postgres database
        db = DatabaseConnection()

        # Change autocommit settings to allow for database creation
        original_autocommit_state = db.my_connection.autocommit
        db.my_connection.autocommit = True

        # Select all database names available
        db.my_cursor.execute("SELECT datname FROM pg_database;")
        database_list = db.my_cursor.fetchall()
        print(database_list)
        print(db_name)
        print((db_name,) in database_list)
#        quit()
        # Create database if it does not exist already
        if not (db_name,) in database_list:
            print('The database named "%s" does not exist. Creating it now...' %
                db_name)
            db_sql = ("""CREATE DATABASE {database};""".format(
                database=db_name))
            db.my_cursor.execute(db_sql)
            db.my_connection.autocommit = original_autocommit_state
            print('Database %s created.' % db_name)
        else:
            print('The database named "%s" already exists.' % db_name)

        # Reset settings (not required) and close connection
        db.my_connection.autocommit = original_autocommit_state
        db.close_connection()

    def check_data_table(db_name, table_name, manual_creation=False):
        """Checks if the data table exists, and if not, creates it.
        Args:
            db_name: name of the database
            table_name: name of the data table
        Returns:
            N/A
        """
        # Connect to DB
        db = DatabaseConnection(db_name)
        print("Checking the data table...")

        if manual_creation:
            create_table_sql_query = ("""
CREATE TABLE IF NOT EXISTS {table_name}(
    PRIMARY KEY(tweet_id),
    tweet_id	    BIGINT			,
    created_at	    TIMESTAMP		,
    screen_name	    TEXT			,
    full_text	    TEXT			,
    retweet_count   INTEGER         ,
    sentiment	    NUMERIC(7, 3));""".format(table_name=table_name))

        else:
            csv_headers = DatabasePopulation.get_csv_column_headers(Config.SOURCE_FILE_NAME)
            sql_column_names = DatabasePopulation.format_sql_column_names(csv_headers)
            create_table_sql_query = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
            for i in range(len(sql_column_names)):
                if i < len(sql_column_names)-1:
                    create_table_sql_query += "\t" + sql_column_names[i] + " varchar(255),\n"
                else:
                    create_table_sql_query += "\t" + sql_column_names[i] + " varchar(255)"
            create_table_sql_query += ");"
#        print (create_table_sql_query)

        db.my_cursor.execute(create_table_sql_query)
        db.close_connection()
        print("Data table check complete, ready to start saving data.")

    def initialize_db(db_name, table_name, reset_db=False):
        """Checks if the database and data table exists,
        and if not, creates it.
        Args:
            db_name: name of the database
            table_name: name of the data table
        Returns:
            db: Connection to the database
        """

        print("Checking for the database... UNCOMMENT OUT THESE NEXT 3 LINES")
#        DatabaseInitialization.reset_database(db_name, reset_db)
#        DatabaseInitialization.check_database(db_name)
#        DatabaseInitialization.check_data_table(db_name, table_name)
        
        db = DatabaseConnection(db_name, table_name)
        return db

"""Functionality for connecting to and storing data in a database"""
class DatabaseConnection():

    def __init__(self, database='postgres', table_name='postgres'):
        try:
            self.my_connection = psycopg2.connect(
                host=Config.POSTGRES_HOST,
                database=database,
                user=Config.POSTGRES_USER,
                password=Config.POSTGRES_PASSWORD,
                port=Config.POSTGRES_PORT
            )
            self.my_cursor = self.my_connection.cursor(cursor_factory=RealDictCursor)
            self.table_name = table_name
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            quit("Exiting program.")

    def close_connection(self):
        """Commits changes to database and closes the connection
        Args:
            self
        Returns:
            N/A
        """

        print("Closing database connection...")
        self.my_connection.commit()
        print("Changed committed to database.")
        self.my_cursor.close()
        print("Database cursor closed.")
        self.my_connection.close()
        print("Database connection closed.")

    def import_csv_data_to_db(self, file_name):
        sql_query = f"COPY      {self.table_name}\
                      FROM      STDIN\
                      DELIMITER ','\
                      CSV       HEADER;"

        with open(file_name,  'rb') as csv_file:
            self.my_cursor.copy_expert(sql_query, csv_file)
        self.my_connection.commit()
        print(f"Data uploaded from {file_name} to {self.table_name}.")

    """TODO: Method may be obsolete"""
    def store_data(self, status):
        """Saves stream data to the database
        Args:
            self
            status: Results from the streamer (i.e., Tweets)
        Returns:
            N/A
        """
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

        print(status.id)
        print(status.created_at)
        print(status.user.screen_name)
        print(text)
        print(retweet_count)
        print(sentiment)
        print("")
        self.my_cursor.execute(
            "insert into %s values (%%s, %%s, %%s, %%s, %%s, %%s)"\
                % quote_ident(table_name, self.my_cursor),
            [status.id, status.created_at, status.user.screen_name, text,
                retweet_count, sentiment])
        self.my_connection.commit()

    def fetch_most_recent(self, limit=1):
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

        # for result in results:
        #     print("")
        #     for item in result:
        #         print(item)

        return results


    def fetch_total_count(self):

        stmt = sql.SQL("""            
            SELECT row_to_json(t)
            FROM (
                SELECT COUNT(*) as total
                FROM {table_name}
            ) t;
        """).format(
            table_name = sql.Identifier(self.table_name)
        )

        self.my_cursor.execute(stmt)
        results = self.my_cursor.fetchall()
        return results

    def fetch_from_db(self, limit=None, sort_desc=None):

        #Inputs
        limit = 5
        sort_desc = True
        sort_by_column = 'ad_requests'
        filter_term = 'TC_Dashboard_160x600_Floor'
        filter_column = 'dfp_ad_units'

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
        if filter_term is not None:
            stmt += sql.SQL("WHERE {filter_column} LIKE {filter_term} ").format(
                filter_column = sql.Identifier(filter_column),
                filter_term = sql.Literal(filter_term + '%%')
                )

        #Sort
        if sort_desc is not None:
            if sort_desc:
                sort_type = "DESC"
            else:
                sort_type = "ASC"
            stmt += sql.SQL("ORDER BY {sort_by_column} {sort_type} ").format(
                sort_by_column = sql.Identifier(sort_by_column),
                sort_type = sql.SQL(sort_type)
                )

        #Limit results
        if limit is not None:
            stmt += sql.SQL("LIMIT %s ")
            data += (limit,)

        stmt += sql.SQL(") t;")

        self.my_cursor.execute(stmt, data)
        results = self.my_cursor.fetchall()
        return results

    @staticmethod
    def get_json_component(results, data_type):

        if data_type == "total":
            chars_to_strip = 3
        elif data_type == "data":
            chars_to_strip = 2
        results_str = json.dumps(results)[chars_to_strip:-chars_to_strip]

        if data_type == "data":
            results_str = "\"rows\": " + results_str

        return results_str

    @staticmethod
    def build_table_json(total_count_str, results_len, results_str):

        results_len_str = "\"totalNotFiltered\": " + str(results_len)
        table_json_str = "{ " + total_count_str + ", " + results_len_str + ", " + results_str + " }"
        return table_json_str


"""Functionality for initial data population in a database"""
class DatabasePopulation():

    """Deprecated method for auto-creating tables in PostgreSQL"""
    @staticmethod
    def create_table_from_csv(db_name, db_url, table_name, file_url):
        subprocess.run([db_name,
                        "--db",
                        db_url,
                        f"{table_name}",
                        f"{file_url}"])

    @staticmethod
    def get_csv_column_headers(source_file_name):
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
    
    #TODO: Might not be used to can be deleted
    @staticmethod
    def get_sql_names_from_file(source_file_name):
        headers = get_csv_column_headers(source_file_name)
        sql_columns = format_sql_column_names(headers)
        return sql_columns

"""Upload data to Google Cloud Storage"""
class GoogleCloud():

    def upload_blob(source_file_name):

        # Upload the file to Google Cloud Storage
        storage_client = storage.Client.from_service_account_json(current_app.config['GCLOUD_CREDENTIALS'])
        bucket_name = current_app.config['GCLOUD_DATA_BUCKET_NAME']
        try:
            bucket = storage_client.get_bucket(bucket_name)
        except:
            print("Whoops, that bucket does not exist, let's create it!")
            bucket = storage_client.create_bucket(bucket_name)
            print(f"{bucket_name} bucket created!")

        """
        bucket_name = 'my_bucket_name'
        bucket = storage_client.bucket(bucket_name)
        stats = storage.Blob(bucket=bucket, name=source_file_name).exists(storage_client)
        """

        bucket = storage_client.bucket(bucket_name)
        file_exists = storage.Blob(bucket=bucket, name=source_file_name).exists(storage_client)

        if file_exists:
            user_wants_to_overwrite = get_user_overwrite_permission()
            if user_wants_to_overwrite:
                blob = bucket.blob(source_file_name) # Name the blob
                blob.upload_from_filename(source_file_name) # Upload the file
                print(f"File {source_file_name} uploaded to {source_file_name}.")
            else:
                print("No file uploaded.")

        if current_app.config['REQUIRE_SIGNED_URL'] == True:
            return generate_download_signed_url_v4(bucket_name, source_file_name)
        elif current_app.config['REQUIRE_SIGNED_URL'] == False:
            return f"https://storage.googleapis.com/{bucket_name}/{source_file_name}"

    @staticmethod
    def get_user_overwrite_permission():
        print("WARNING: The file already exists. Do you want to overwrite it?")
        user_input = input("TYPE 'YES' TO OVERWRITE: ")
        if user_input == "YES":
            return True
        else:
            return False