from ..db import DB
from flask import Blueprint, render_template

community_bp = Blueprint("community", __name__, template_folder="templates")


def register_routes(db: DB):
    @community_bp.route("/")
    def index():
        return render_template("community.html")
        pass
