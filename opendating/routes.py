from flask import render_template, request
from .util import random_hex_color
from .db import DB, Chat, Message

       
def configure_api_and_processors(app, db: DB):
    @app.route("/active_user", methods=['GET' ,'POST'])
    def active_user():
        if request.method == "POST":
            data = request.get_json()
            print(data)
            db.current_username = data['id']
            db.save()
            return {}, 200 
        elif request.method=="GET":
            return {id: db.current_username}

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
        return {'users': db.users, 'active_user': db.get_user_by_username(db.current_username)}

    @app.context_processor
    def inject_chat_users():
        message_users = [] 
        for user in db.users: 
            active = False
            if user.username == db.current_username: 
                active = True
            
            color = random_hex_color(['#FFFFFF', '#F5F5F5', '#E0E7FF', '#F4F4F4', '#efffaf','#00fef4'])
            message_users.append({"user": user, "color": color, "active": active, "initial": user.name[0]})

        return {'msg_users': message_users}

            
        



