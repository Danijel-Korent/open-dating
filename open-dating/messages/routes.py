from flask import Blueprint, render_template
from ..db import DB

messages_bp = Blueprint("messages", __name__, template_folder="templates")

def register_routes(db: DB):
    @messages_bp.route("/")
    def messages():
        return render_template("messages.html", title="Messages", chats=db.get_match_chats())

    @messages_bp.route("/<user>")
    def chat(user):
        db_user = db.get_user_by_username(user)
        if db_user != None:
            return render_template("chat.html", title="Chat with " + db_user.name, user=db_user, chat=db.get_chat(db_user.username)) 
        else: 
            return "User not found"

    @messages_bp.route("/community")
    def community(user):
        return render_template("community.html") 



 
