from flask import Flask, render_template, request
import logging
import sys
import json
import random

from db import DB 

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

db = DB()

@app.route("/")
def home():
    return render_template("pages/index.html", title="Dating App") 

@app.route("/community")
def community(): 
    return render_template("pages/community.html", messages=db.messages2, get_user_by_id=get_user_by_id, current_id=db.current_id, title="Community Chat")

@app.route("/announcements")
def announcements(): 
    return render_template("pages/announcements.html", title="Announcements")

@app.route("/active_user", methods=['GET' ,'POST'])
def active_user():
    if request.method == "POST":
        db.current_id = request.form['id']
        db.save()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    elif request.method=="GET":
        return {id: db.current_id}

@app.context_processor
def inject_users():
    return {'users': db.users, 'active_user': db.get_user_by_id(db.current_id)}

@app.context_processor
def inject_chat_users():
    message_users = [] 
    for user in db.users: 
        active = False
        if user["id"] == db.current_id: 
            active = True
        
        color = random_hex_color(['#FFFFFF', '#F5F5F5', '#E0E7FF', '#F4F4F4', '#efffaf','#00fef4'])
        message_users.append({"user": user, "color": color, "active": active, "initial": user["name"][0]})

    return {'msg_users': message_users}

def get_user_by_id(users, id):
    for user in users:
        if user['user']['id'] == id:
            return user

def random_hex_color(excluded_colors):
    while True:
        # Generate random hex color
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF)).upper()
        # Check if it's in the excluded list
        if color not in excluded_colors:
            return color
        else:
            return random_hex_color(excluded_colors)


if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=8080, debug=True) 


