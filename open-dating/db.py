import json
import sys
from typing import Dict
from dataclasses import dataclass, asdict
from enum import Enum

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
    seen_users: list[str]

    def __init__(self, filename="mock_database.json"):
        self.filename=filename
        self.current_username = ""
        self.users = []
        self.likes = []
        self.seen_users = []
        self.matches = []
        self.chawts = [] 
        self.load() 

    def load(self):
        print("Loaded DB")
        with open(self.filename) as db:
            d = json.load(db)
            self.from_json(d)
            db.close()
    
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
                    )
                )
                for user in json_dict["users"]
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
        with open(self.filename,"r+") as db:
            db.seek(0)
            db.truncate()
            new_db = asdict(self)
            new_db.pop('filename')
            json.dump(new_db, db, indent=4)

    def get_user_by_username(self,username) -> User | None:
        for user in self.users:
            if user.username == username:
                return user
        return None

    def get_current_user_matches(self):
        matches = []
        for match in self.matches:
            if match.user1 == self.current_username:
                matches.append(self.get_user_by_username(match.user2))
            if match.user2 == self.current_username:
                matches.append(self.get_user_by_username(match.user1))


        return matches

    def get_user_chats(self):
        chats = self.chats
        matches = self.get_current_user_matches()  

        chats_final = []

        for match in matches:
            chat = self.get_user_chat(match.username)
            if chat == None:
                chat = {}
            chats_final.append({"user": match, "chat": chat})


        return chats_final



    def get_user_chat(self, username: str):
        for chat in self.chats:
               if chat.user1 == username and chat.user2 == self.current_username:
                    return chat
               if chat.user1 == self.current_username and chat.user2 == username:
                    return chat

        return None

    def get_recommended_user(self):
        for user in self.users:
            if self.validate_user_recommendation(user) == True:
                return user

    def validate_user_recommendation(self, user) -> bool:
        if user.username in self.seen_users:
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





