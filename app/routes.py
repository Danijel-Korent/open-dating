from flask import render_template, request, session
from .util import random_hex_color
from .db import DB, Chat, Message

       
def configure_api_and_processors(app, db: DB):
    @app.before_request
    def ensure_current_user():
        if 'username' not in session:
            session['username'] = db.default_username

    @app.route("/active_user", methods=['GET' ,'POST'])
    def active_user():
        if request.method == "POST":
            data = request.get_json()
            print(data)
            session['username'] = data['id']
            db.save()
            return {}, 200 
        elif request.method=="GET":
            return {id: session['username']}

    @app.route("/reload_json", methods=['POST']) 
    def reload_json():
        if request.method == "POST":
            db.load()
            return {}, 200 

    @app.context_processor
    def inject_get_image_path():
        return dict(get_image_path=db.get_image_path) 
    

    @app.context_processor
    def inject_users():
        return {'users': db.users, 'active_user': db.get_user_by_username(session['username'])}
   



