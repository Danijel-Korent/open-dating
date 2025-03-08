from ..db import DB
from flask import Blueprint, render_template

communities_bp = Blueprint("community", __name__, template_folder="templates")


def register_routes(db: DB):
    @communities_bp.route("/")
    def index():
        return render_template("community/index.html", title="Communities")

    @communities_bp.route("/community/<name>")
    def community(name):
        return render_template(
            "community/community.html", community_name=name, title=name
        )

    @communities_bp.route("/community/<name>/members")
    def community_members(name):
        return render_template(
            "community/members.html", community_name=name, title="Members of %s" % name
        )
