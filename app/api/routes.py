from flask import (
    Blueprint,
    Response,
    json,
    jsonify,
    make_response,
    render_template,
    render_template_string,
    request,
)
from ..db import DB, GenderPreference, Preferences, preference_filter

api_bp = Blueprint("api", __name__)


def register_routes(db: DB):
    @api_bp.route("/preferences", methods=["GET", "POST"])
    def preferences():
        if request.method == "POST":
            print(request.form)
            form = request.form
            male = False
            female = False
            nonbinary = False
            if form.get("male", False):
                male = True
            if form.get("female", False):
                female = True
            if form.get("nonbinary", False):
                nonbinary = True
            r_preferences = Preferences(
                age_min=int(float(form["age-min"])),
                age_max=int(float(form["age-max"])),
                distance_meters=int(float(form["distanceKms"]) * 1000),
                gender=GenderPreference(
                    male,
                    female,
                    nonbinary,
                ),
            )
            db.get_current_user().preferences = r_preferences
            db.save()
            return render_template_string(
                """
                 {% from "includes/macros.html" import preferences_form with context %}
            
                 {{preferences_form(r_preferences)}}

                 <script>
                    window.lucide()
                 </script>
            """,
                r_preferences=r_preferences,
            )
        return make_response(400)

    @api_bp.route("/get_interest/<id>", methods=["GET"])
    def get_interest(id: str):
        for interest in db.interests:
            if interest.id == id:
                return json.dumps(interest)

        return make_response(400)

    @api_bp.route("/next_user")
    def next_user():
        next_user = db.get_recommended_user()

        return make_response(200)

    @api_bp.route("/all_users", methods=["GET"])
    def all_users():
        users = db.users

        if db.get_current_user() in users:
            users.remove(db.get_current_user())

        return users

    @api_bp.route("/all_users/filtered", methods=["GET"])
    def filtered_users():
        users = db.users
        return make_response(preference_filter(db.get_current_user(), users))
