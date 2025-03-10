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

from .db import DB, init_new_db
from .routes import configure_api_and_processors
from .config import Config
from .dating import routes as dating
from .messages import routes as messages
from .communities import routes as communities
from .api import routes as api

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

socketio = SocketIO()
compress = Compress()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = os.getenv("SECRET")
    app.secret_key = os.urandom(24)  # Generates a random 24-byte key

    database = DB(app.config.get("DATABASE_FILE"))

    add_cmdline_options(app, database)

    dating.register_routes(database)
    app.register_blueprint(dating.dating_bp)
    messages.register_routes(database, socketio)
    app.register_blueprint(messages.messages_bp, url_prefix="/messages")
    communities.register_routes(database)
    app.register_blueprint(communities.communities_bp, url_prefix="/communities")
    api.register_routes(database)
    app.register_blueprint(api.api_bp, url_prefix="/api")

    configure_api_and_processors(app, database)

    socketio.init_app(app)
    compress.init_app(app)

    return app


def add_cmdline_options(app: App, db: DB):
    db_cli = AppGroup("db")

    @db_cli.command("select-database")
    @click.argument("path")
    def select_database(path):
        load_dotenv()
        set_key(".env", "DATABASE_FILE", path)
        print("Set DATABASE_FILE in .env to ", path)
        exit()

    @db_cli.command("init-db")
    @click.argument("path")
    def init_db(path: str):
        init_new_db(path)
        print("Created new database at ", path)
        exit()

    @click.command("gen-secret")
    def gen_secret():
        load_dotenv()
        set_key(".env", "SECRET", uuid.uuid4().hex)
        print("Generated secret key and set in .env")
        exit()

    @click.command("reset-db")
    def reset_db():
        reset_db(db)
        print("Reset database chats, likes, matches, and seen users")
        exit()

    app.cli.add_command(db_cli)
    app.cli.add_command(gen_secret)


app = create_app()
