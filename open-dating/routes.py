from flask import render_template, request
from .util import random_hex_color
from .db import DB

def configure_page_routes(app, db: DB):
    @app.route("/")
    def home():
        return render_template("pages/index.html", title="Recommended") 

    @app.route("/community")
    def community(): 
        return render_template("pages/community.html", messages=db.messages2, get_user_by_username=db.get_user_by_username, current_username=db.current_username, title="Community")

    @app.route("/announcements")
    def announcements(): 
        return render_template("pages/announcements.html", title="Announcements")

    @app.route("/matches")
    def matches():
        return render_template("pages/matches.html", title="Matches", matches=db.get_current_user_matches())

    @app.route("/messages")
    def messages():
        return render_template("pages/messages.html", title="Messages",chats=db.get_user_chats())

    @app.route("/messages/<user>")
    def chat(user):
        db_user = db.get_user_by_username(user)
        if db_user != None:
            return render_template("pages/chat.html", title="Chat with " + db_user['name'], user=db_user) 
        else: 
            return "User not found"



        
def configure_api_and_processors(app, db):
    @app.route("/active_user", methods=['GET' ,'POST'])
    def active_user():
        if request.method == "POST":
            db.current_username = request.form['id']
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
    def inject_users():
        return {'users': db.users, 'active_user': db.get_user_by_username(db.current_username)}

    @app.context_processor
    def inject_chat_users():
        message_users = [] 
        for user in db.users: 
            active = False
            if user["username"] == db.current_username: 
                active = True
            
            color = random_hex_color(['#FFFFFF', '#F5F5F5', '#E0E7FF', '#F4F4F4', '#efffaf','#00fef4'])
            message_users.append({"user": user, "color": color, "active": active, "initial": user["name"][0]})

        return {'msg_users': message_users}


