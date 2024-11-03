from flask import Flask, render_template, request, make_response
from flask.sansio.app import App
from flask.cli import AppGroup
from dotenv import load_dotenv, set_key
import click
import logging

from .db import DB 
from .routes import configure_api_and_processors
from .config import Config
from .dating import routes
from .messages import routes

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    add_cmdline_options(app)

    database = DB(app.config.get("DATABASE_FILE"))
   
    dating.routes.register_routes(database)
    app.register_blueprint(dating.routes.dating_bp)
    messages.routes.register_routes(database)
    app.register_blueprint(messages.routes.messages_bp, url_prefix="/messages")


    
    configure_api_and_processors(app, database)

    return app

def add_cmdline_options(app: App):
    db_cli = AppGroup('db')
    @db_cli.command("select-database")
    @click.argument("path")
    def select_database(path):
        load_dotenv()
        set_key(".env", "DATABASE_FILE", path)
        print("Set DATABASE_FILE in .env to ", path)

    app.cli.add_command(db_cli)

