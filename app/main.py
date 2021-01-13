#!/usr/bin/env python

from flask import Flask

import config
from routes import main

def create_app():
    env = "production"

    app = Flask(__name__, static_url_path='')
    if env == "production":
        app.config.from_object(config.ProductionConfig)
    elif env == "development":
        app.config.from_object(config.DevelopmentConfig)
    else:
        raise ValueError('Invalid environment name')

    # db.init_app(app)
    app.register_blueprint(main)
    app.register_error_handler(403, main.page_forbidden)
    app.register_error_handler(404, main.page_not_found)
    app.register_error_handler(500, main.internal_server_error)
    app.register_error_handler(503, main.service_unavailable)

    return app

app = create_app()

if __name__ == "__main__":
    # app.run(host="localhost", port=5000, debug=app.config['DEBUG_STATUS'])
    app.run()
