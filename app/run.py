#!/usr/bin/env python

# from app import create_app, db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    created_app = Flask(__name__, static_url_path='')
    created_app.config.from_object(Config)
    db.init_app(created_app)

    from main.routes import main
    created_app.register_blueprint(main)
    return created_app


app = create_app()

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=app.config['DEBUG_STATUS'])
