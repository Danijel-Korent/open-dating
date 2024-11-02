from flask import Blueprint, render_template
from ..db import DB

dating_bp = Blueprint("dating", __name__, template_folder="templates")

def register_routes(db: DB):
    @dating_bp.route("/")
    def dating_home():
        user = db.get_recommended_user()
        return render_template("index.html", user=user, title="Profiles") 

    @dating_bp.route("/matches")
    def dating_matches():
        return render_template("matches.html", matches=db.get_match_users()) 


