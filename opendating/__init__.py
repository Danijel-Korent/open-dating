import os
from flask import Flask, render_template, request, make_response
from flask.sansio.app import App
from flask.cli import AppGroup
from dotenv import load_dotenv, set_key
import click
import logging
from flask_socketio import SocketIO
from flask_compress import Compress
import uuid

from .db import DB 
from .routes import configure_api_and_processors
from .config import Config
from .dating import routes
from .messages import routes

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

socketio = SocketIO()
compress = Compress()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = os.getenv("SECRET")
    add_cmdline_options(app)

    database = DB(app.config.get("DATABASE_FILE"))
   
    dating.routes.register_routes(database)
    app.register_blueprint(dating.routes.dating_bp)
    messages.routes.register_routes(database, socketio)
    app.register_blueprint(messages.routes.messages_bp, url_prefix="/messages")



    
    configure_api_and_processors(app, database)

    socketio.init_app(app)
    compress.init_app(app)
    
    return app


def add_cmdline_options(app: App):
    db_cli = AppGroup('db')
    @db_cli.command("select-database")
    @click.argument("path")
    def select_database(path):
        load_dotenv()
        set_key(".env", "DATABASE_FILE", path)
        print("Set DATABASE_FILE in .env to ", path)

    @click.command("gen-secret")
    def gen_secret():
        load_dotenv()
        set_key(".env", "SECRET", uuid.uuid4().hex)
        print("Generated secret key and set in .env")

    app.cli.add_command(db_cli)
    app.cli.add_command(gen_secret)


