#!/usr/bin/env python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.database import DatabasePopulation, DatabaseInitialization

db = DatabaseInitialization.initialize_db(
    Config.DB_NAME, Config.TABLE_NAME, Config.RESET_DB)
db.import_csv_data_to_db(Config.SOURCE_FILE_NAME)
results = db.fetch_most_recent(10000000000)
#print(results)

db.close_connection()

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='')
    app.config.from_object(Config)
    db.init_app(app)

    from app.main.routes import main
    app.register_blueprint(main)
    return app