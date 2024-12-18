from ..db import DB
from flask import Blueprint, render_template

communities_bp = Blueprint("community", __name__, template_folder="templates")


def register_routes(db: DB):
    @communities_bp.route("/")
    def index():
        return render_template("index.html")

    @communities_bp.route("/community/<name>")
    def community(name):
        return render_template("community.html", community_name=name)
