#!/usr/bin/env python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='')
    app.config.from_object(Config)

    # import os
    # print(app.config["SSL_REDIRECT"])
    # print(app.config["SECRET_KEY"])
    # print(app.config["GCLOUD_CREDENTIALS"])
    # quit()

    db.init_app(app)

    from app.main.routes import main
    app.register_blueprint(main)
    return app
