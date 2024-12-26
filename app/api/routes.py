from flask import Blueprint, Response, jsonify, make_response, request
from ..db import DB

api_bp = Blueprint("api", __name__)


def register_routes(db: DB):
    @api_bp.route("/preferences", methods=["GET", "POST"])
    def preferences():
        if request.method == "GET":
            return jsonify(db.get_current_user().preferences)
        if request.method == "POST":
            preferences = request.form["preferences"]
            print(preferences)
            return make_response(200)

        return make_response(400)
