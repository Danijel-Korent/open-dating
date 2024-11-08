from dataclasses import asdict
from typing import Any
from flask import Blueprint, Response, jsonify, render_template, request
from ..db import DB, Like, Match, User
import json

dating_bp = Blueprint("dating", __name__, template_folder="templates")

def register_routes(db: DB):
    @dating_bp.route("/")
    def index():
        user = db.get_recommended_user()
        return render_template("index.html", user=user, title="Profiles") 

    @dating_bp.route("/<user>")
    def user(user):
        user = db.get_user_by_username(user)
        return render_template("user.html", user=user, title=user.name)

    @dating_bp.route("/<user>/react", methods=["POST"])
    def react_user(user):
        data = request.get_json()
        if data['type'] == "like":
            for like in db.likes:
                if like.liked==db.current_username and like.liker==user:
                    db.likes.remove(like)
                    db.matches.append(Match(user1=db.current_username, user2=user, match_date=""))
                    db.get_user_by_username(db.current_username).seen_users.append(user)
                    db.save()
                    return Response(
                        response=json.dumps({"match": True}),
                        status=200,
                        mimetype='application/json'
                    ) 


            db.get_user_by_username(db.current_username).seen_users.append(user)
            db.likes.append(Like(liker=db.current_username, liked=user, timestamp=""))
            db.save()
            return jsonify({"match": False}), 200
        if data['type'] == "nope":
            db.get_user_by_username(db.current_username).seen_users.append(user)
            db.save()
            return Response(
                        response=json.dumps({"match": False}),
                        status=200,
                        mimetype='application/json'
                    )
        return {}, 400

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
        return {}, 200 


