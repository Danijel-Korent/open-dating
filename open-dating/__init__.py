from flask import Flask, render_template, request, make_response
import logging

from .db import DB 
from .config import Config
from .routes import configure_api_and_processors, configure_page_routes

logging.basicConfig(level=logging.DEBUG)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db = DB()

    configure_page_routes(app, db)
    configure_api_and_processors(app, db)

    return app

