from flask import Blueprint, render_template, request, session
from ..db import DB, Message, Chat
from flask_socketio import SocketIO, send, emit
from typing import Dict

messages_bp = Blueprint("messages", __name__, template_folder="templates")


def register_routes(db: DB, socketio: SocketIO):
    @messages_bp.route("/")
    def messages():
        return render_template(
            "messages.html", title="Messages", chats=db.get_match_chats()
        )

    @messages_bp.route("/<user>")
    def chat(user):
        db_user = db.get_user_by_username(user)
        if db_user != None:
            return render_template(
                "chat.html",
                title="Chat with " + db_user.name,
                user=db_user,
                chat=db.get_chat(db_user.username),
            )
        else:
            return "User not found"

    @messages_bp.route("/<user>/send", methods=["POST"])
    def send_message(user):
        chat = db.get_chat(user)
        body = request.get_json()
        message = body["message"]
        curr_user = session["username"]
        print(message, " sent!")
        if chat != None:
            chat.messages.append(
                Message(
                    sender_id=curr_user, receiver_id=user, timestamp="", message=message
                )
            )
            db.save()
        else:
            db.chats.append(
                Chat(
                    user1=user,
                    user2=curr_user,
                    messages=[
                        Message(
                            sender_id=curr_user,
                            receiver_id=user,
                            timestamp="",
                            message=message,
                        )
                    ],
                )
            )
        return {}, 200

    @socketio.on("chatmessage")
    def message(message):
        sender = message["sender_id"]
        recipient = message["receiver_id"]
        message = message["message"]

        print(len(message))
        if len(message) == 0:
            return

        chat = db.get_chat_between(sender, recipient)
        if chat != None and message != None:
            chat.messages.append(
                Message(
                    sender_id=sender,
                    receiver_id=recipient,
                    message=message,
                    timestamp="",
                )
            )
            socketio.emit(
                "messagereceived",
                {"sender_id": sender, "receiver_id": recipient, "message": message},
            )
        elif chat == None and message != None:
            db.chats.append(
                Chat(
                    user1=sender,
                    user2=recipient,
                    messages=[
                        Message(
                            sender_id=sender,
                            receiver_id=recipient,
                            timestamp="",
                            message=message,
                        )
                    ],
                )
            )

        db.save()
