import json
import os
import sys
from typing import Dict
from dataclasses import dataclass, asdict
from enum import Enum
from flask import url_for
from werkzeug.utils import secure_filename
    

@dataclass
class Preferences:
    gender: str
    age_max: int
    age_min: int
    distance_meters: int

    def check_user(self, user:"User") -> bool:
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
    preferences: Preferences
    seen_users: list[str]

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
    current_username: str
    matches: list[Match]
    likes: list[Like]
    chats: list[Chat]

    def __init__(self, filename):
        self.filename=filename
        self.current_username = ""
        self.users  =  []
        self.likes = []
        self.matches = []
        self.chats = [] 

        if not os.path.exists(self.filename):
            self.save()
        self.load()

    def load(self):
        with open(self.filename, "r") as file:
            self.from_json(json.load(file))
        print("Loaded DB")

    def from_json(self, json_dict: dict):
        self.current_username = json_dict['current_username']
        for user in json_dict['users']:
            self.users = [
                User(
                    username=user['username'], 
                    name=user['name'],
                    age=user['age'],
                    gender=user['gender'],
                    location=user['location'],
                    bio=user['bio'],
                    likes=[],
                    pictures=user['pictures'],
                    preferences=Preferences(
                        gender=user['preferences']['gender'],
                        age_min=user['preferences']['age_min'],
                        age_max=user['preferences']['age_max'],
                        distance_meters=user['preferences']['distance_meters']
                    ),
                    seen_users=[]
                )
                for user in json_dict["users"]
            ]
        self.likes = [
            Like(
                liker=like['liker'],
                liked=like['liked'],
                timestamp=""
            )
            for like in json_dict['likes']
        ]
        self.matches = [
            Match(
                user1=match['user1'],
                user2=match['user2'],
                match_date=match['match_date']
            )
            for match in json_dict['matches']
        ]

        self.chats = [
                Chat(
                    user1=chat['user1'],
                    user2=chat['user2'],
                    messages=[
                        Message(
                            sender_id=msg['sender_id'],
                            receiver_id=msg['receiver_id'],
                            timestamp=msg['timestamp'],
                            message=msg['message']
                        )
                        for msg in chat['messages']
                    ]
                )
                for chat in json_dict['chats']
            ]

    def save(self):
        with open(self.filename, "w+") as file:
            new_db = asdict(self)
            new_db.pop('filename')
            json_str = json.dumps(new_db, indent=4)
            file.write(json_str)

    def get_user_by_username(self,username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user

        return User(username="user_missing", name="User Missing", age=0, gender="", location="", bio="", preferences=Preferences(age_min=0, age_max=0, gender="", distance_meters=0), likes=[], pictures=[], seen_users=[])

    def get_current_user(self) -> User:
        return self.get_user_by_username(self.current_username)


    def get_match_users(self):
        matches: list[User] = []
        for match in self.matches:
            if match.user1 == self.current_username:
                matches.append(self.get_user_by_username(match.user2))
            if match.user2 == self.current_username:
                matches.append(self.get_user_by_username(match.user1))


        return matches

    def get_like_users(self) -> list[User]:
        likes: list[User] = []
        for like in self.likes:
            if like.liker != self.current_username and like.liked == self.current_username:
                likes.append(self.get_user_by_username(like.liker))
        return likes

    def get_match_chats(self):
        matches = self.get_match_users()  

        chats = []

        for match in matches:
            chat = self.get_chat(match.username)
            if chat == None:
                chat = {}
            else:
                chats.append({"user": match, "chat": chat})

        return chats

    def get_chat(self, with_username: str) -> Chat | None:
        for chat in self.chats:
               if chat.user1 == with_username and chat.user2 == self.current_username:
                    return chat
               if chat.user1 == self.current_username and chat.user2 == with_username:
                    return chat

        return None

    def get_recommended_user(self):
        for user in self.users:
            if self.validate_user_recommendation(user) == True:
                return user

    def validate_user_recommendation(self, user) -> bool:
        if user.username in self.get_current_user().seen_users:
            return False
        if user.username == self.current_username:
            return False 
        for like in self.likes:
            if like.liked == user.username:
                return False
        for match in self.matches:
            if match.user1 == user.username and match.user2 == self.current_username:
                return False 
            if match.user2 == user.username and match.user1 == self.current_username:
                return False
        if self.get_user_by_username(self.current_username).preferences.check_user(user) != True:
            return False

        return True

    def swipe_user(self, user: str, action_type: int) -> bool:
        self.get_current_user().seen_users.append(user)
        if action_type == 1:
            self.get_user_by_username(user).likes.append(Like(liker=self.current_username, liked=user, timestamp=""))
            for like in self.get_current_user().likes:
                if like.liker == user:
                    return True

        return False
    
    def get_image_path(self, user: str, image_name: str):
        if image_name == None:
            return ""
        user_obj = self.get_user_by_username(user)
        pictures = user_obj.pictures
        return url_for("static", filename=os.path.join("images", user_obj.username, image_name))

    def set_user_image(self, image, index: int):
        filename = secure_filename(image.filename)
        path = self.get_image_path(self.current_username, filename)
        image.save(os.path.join(path, filename))
        if index > len(self.get_user_by_username(self.current_username).pictures)-1:
            self.get_user_by_username(self.current_username).pictures.append(filename)
        else: 
            self.get_user_by_username(self.current_username).pictures[index] = filename





