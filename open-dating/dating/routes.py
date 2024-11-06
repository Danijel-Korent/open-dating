from flask import Blueprint, render_template, request
from ..db import DB

dating_bp = Blueprint("dating", __name__, template_folder="templates")

def register_routes(db: DB):
    @dating_bp.route("/")
    def index():
        user = db.get_recommended_user()
        return render_template("index.html", user=user, title="Profiles") 

    @dating_bp.route("/likes")
    def likes():
        return render_template("matches_likes.html", likes=db.get_like_users(), matches=db.get_match_users(), title="Likes & Matches") 

    @dating_bp.route("/profile")
    def profile():
        return render_template("profile.html", title="Profile", current_user=db.get_current_user())

    @dating_bp.route("/profile/edit_profile", methods=['POST'])
    def edit_profile():
        index = 0
        for file in request.files:
            db.set_user_image(file, index)
            index = index + 1
        pass


