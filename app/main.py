#!/usr/bin/env python

# from app import create_app, db
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# from config import ProductionConfig, DevelopmentConfig
import config
from routes import main

# db = SQLAlchemy()

def create_app():
    env = "development"

    app = Flask(__name__, static_url_path='')
    if env == "production":
        app.config.from_object(config.ProductionConfig)
    elif env == "development":
        app.config.from_object(config.DevelopmentConfig)
    else:
        raise ValueError('Invalid environment name')

    # db.init_app(app)
    app.register_blueprint(main)
    return app

app = create_app()

if __name__ == "__main__":
    # app.run(host="localhost", port=5000, debug=app.config['DEBUG_STATUS'])
    app.run()
