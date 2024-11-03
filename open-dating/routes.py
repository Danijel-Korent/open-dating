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
        print("Hello")
        if request.method == "POST":
            db.load()
            return {}, 200 

    @app.route("/messages/<user>/send", methods=['POST', 'GET']) 
    def send_message(user):
        chat = db.get_chat(user)
        message = request.form['message']
        if chat != None:
            chat.messages.append(Message(sender_id=db.current_username, receiver_id=user, timestamp="", message=message))
            db.save()
        else:
            db.chats.append(Chat(user1=user,user2=db.current_username,messages=[Message(sender_id=db.current_username, receiver_id=user, timestamp="", message=message)]))
        return {},200



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

            
        



