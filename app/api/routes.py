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
from ..db import DB, GenderPreference, Preferences

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
