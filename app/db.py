import json
import os
import sys
from typing import Dict
from dataclasses import dataclass, asdict
from enum import Enum
from flask import url_for, session
from werkzeug.utils import secure_filename


@dataclass
class GenderPreference:
    male: bool
    female: bool
    nonbinary: bool


@dataclass
class Preferences:
    gender: GenderPreference
    age_max: int
    age_min: int
    distance_meters: int

    def check_user(self, user: "User") -> bool:
        if user.age > self.age_max or user.age < self.age_min:
            return False
        if user.gender != self.gender:
            return False
        return True


@dataclass
class User:
    username: str
    name: str
    age: int
    gender: str
    location: str
    bio: str
    likes: list["Like"]
    pictures: list[str]
    interests: list["Interest"]
    preferences: Preferences
    seen_users: list[str]


@dataclass
class Interest:
    name: str
    icon: str | None


@dataclass
class Like:
    liker: str
    liked: str
    timestamp: str


@dataclass
class Match:
    user1: str
    user2: str
    match_date: str


@dataclass
class Message:
    sender_id: str
    receiver_id: str
    timestamp: str
    message: str


@dataclass
class Chat:
    user1: str
    user2: str
    messages: list[Message]


@dataclass
class DB:
    filename: str
    users: list[User]
    default_username: str
    matches: list[Match]
    likes: list[Like]
    chats: list[Chat]
    interests: list[Interest]

    def __init__(self, filename):
        self.filename = filename
        self.default_username = ""
        self.users = []
        self.likes = []
        self.matches = []
        self.chats = []
        self.interests = []

        if not os.path.exists(self.filename):
            self.save()
        self.load()

    def load(self):
        with open(self.filename, "r") as file:
            self.from_json(json.load(file))
        print("Loaded DB")

    def from_json(self, json_dict: dict):
        self.default_username = json_dict["default_username"]
        for user in json_dict["users"]:
            self.users = [
                User(
                    username=user["username"],
                    name=user["name"],
                    age=user["age"],
                    gender=user["gender"],
                    location=user["location"],
                    bio=user["bio"],
                    likes=[],
                    pictures=user["pictures"],
                    interests=user["interests"],
                    preferences=Preferences(
                        gender=GenderPreference(
                            male=user["preferences"]["gender"]["male"],
                            female=user["preferences"]["gender"]["female"],
                            nonbinary=user["preferences"]["gender"]["nonbinary"],
                        ),
                        age_min=user["preferences"]["age_min"],
                        age_max=user["preferences"]["age_max"],
                        distance_meters=user["preferences"]["distance_meters"],
                    ),
                    seen_users=[],
                )
                for user in json_dict["users"]
            ]
        self.likes = [
            Like(liker=like["liker"], liked=like["liked"], timestamp="")
            for like in json_dict["likes"]
        ]
        self.matches = [
            Match(
                user1=match["user1"],
                user2=match["user2"],
                match_date=match["match_date"],
            )
            for match in json_dict["matches"]
        ]

        self.chats = [
            Chat(
                user1=chat["user1"],
                user2=chat["user2"],
                messages=[
                    Message(
                        sender_id=msg["sender_id"],
                        receiver_id=msg["receiver_id"],
                        timestamp=msg["timestamp"],
                        message=msg["message"],
                    )
                    for msg in chat["messages"]
                ],
            )
            for chat in json_dict["chats"]
        ]

        for interest in json_dict["interests"]:
            icon = None
            if "icon" in interest:
                icon = interest["icon"]
            self.interests.append(Interest(name=interest["name"], icon=icon))

    def save(self):
        with open(self.filename, "w+") as file:
            new_db = asdict(self)
            new_db.pop("filename")
            json_str = json.dumps(new_db, indent=4)
            file.write(json_str)

    def get_user_by_username(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user

        return User(
            username="user_missing",
            name="User Missing",
            age=0,
            gender="",
            location="",
            bio="",
            preferences=Preferences(
                age_min=0,
                age_max=0,
                gender=GenderPreference(False, False, False),
                distance_meters=0,
            ),
            likes=[],
            pictures=[],
            seen_users=[],
        )

    def get_current_user(self) -> User:
        return self.get_user_by_username(session["username"])

    def set_preferences(self, preferences):
        self.get_user_by_username(session["username"]).preferences = preferences
        self.save()

    def get_preferences(self):
        return self.get_user_by_username(session["username"]).preferences

    def get_match_users(self):
        matches: list[User] = []
        for match in self.matches:
            if match.user1 == session["username"]:
                matches.append(self.get_user_by_username(match.user2))
            if match.user2 == session["username"]:
                matches.append(self.get_user_by_username(match.user1))

        return matches

    def get_like_users(self) -> list[User]:
        likes: list[User] = []
        for like in self.likes:
            if like.liker != session["username"] and like.liked == session["username"]:
                likes.append(self.get_user_by_username(like.liker))
        return likes

    def get_match_chats(self):
        matches = self.get_match_users()

        chats = []

        for match in matches:
            chat = self.get_chat(match.username)
            if chat is None:
                chat = {}
            else:
                chats.append({"user": match, "chat": chat})

        return chats

    def get_chat(self, with_username: str) -> Chat | None:
        return self.get_chat_between(session["username"], with_username)

    def get_chat_between(self, user1: str, user2: str) -> Chat | None:
        for chat in self.chats:
            if chat.user1 == user1 and chat.user2 == user2:
                return chat
            if chat.user1 == user2 and chat.user2 == user1:
                return chat

    def get_valid_user_recommendations(self):
        users = []
        for user in self.users:
            if self.validate_user_recommendation(user):
                users.append(user)
        return users

    def get_recommended_user(self):
        for user in self.users:
            if self.validate_user_recommendation(user):
                return user

    def validate_user_recommendation(self, user) -> bool:
        if user.username in self.get_current_user().seen_users:
            return False
        if user.username == session["username"]:
            return False
        for like in self.likes:
            if like.liked == user.username:
                return False
        for match in self.matches:
            if match.user1 == user.username and match.user2 == session["username"]:
                return False
            if match.user2 == user.username and match.user1 == session["username"]:
                return False
        if not self.get_user_by_username(session["username"]).preferences.check_user(
            user
        ):
            return False

        return True

    def swipe_user(self, user: str, action_type: int) -> bool:
        self.get_current_user().seen_users.append(user)
        if action_type == 1:
            self.get_user_by_username(user).likes.append(
                Like(liker=session["username"], liked=user, timestamp="")
            )
            for like in self.get_current_user().likes:
                if like.liker == user:
                    return True

        return False

    def get_image_path(self, user: str, image_name: str):
        if image_name == None:
            return ""
        user_obj = self.get_user_by_username(user)
        pictures = user_obj.pictures
        return url_for(
            "static", filename=os.path.join("images", user_obj.username, image_name)
        )

    def set_user_image(self, image, index: int):
        filename = secure_filename(image.filename)
        path = self.get_image_path(session["username"], filename)
        image.save(os.path.join(path, filename))
        if index > len(self.get_user_by_username(session["username"]).pictures) - 1:
            self.get_user_by_username(session["username"]).pictures.append(filename)
        else:
            self.get_user_by_username(session["username"]).pictures[index] = filename
