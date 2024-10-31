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

@dataclass
class User:
    username: str
    name: str
    age: int
    gender: str
    location: str
    bio: str
    pictures: list[str]
    preferences: Preferences

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
    messages: list[Message]

@dataclass
class DB: 
    filename: str
    users: list[User]
    current_username: str
    matches: list[Match]
    chats: list[Chat]

    def __init__(self, filename="mock_database.json"):
        self.filename=filename
        self.current_username = ""
        self.users = []
        self.matches = []
        self.chats = [] 
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
            self.users.append(
                User(
                    username=user['username'], 
                    name=user['name'],
                    age=user['age'],
                    gender=user['gender'],
                    location=user['location'],
                    bio=user['bio'],
                    pictures=user['pictures'],
                    preferences=Preferences(
                        gender=user['preferences']['gender'],
                        age_min=user['preferences']['age_min'],
                        age_max=user['preferences']['age_max'],
                        distance_meters=user['preferences']['distance_meters']
                    )
                )
            )
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
                    messages=[
                        Message(
                            sender_id=msg['sender_id'],
                            receiver_id=msg['receiver_id'],
                            timestamp=msg['timestamp'],
                            message=msg['message']
                        )
                        for msg in conversation['messages']
                    ]
                )
                for conversation in json_dict['chats']
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
            if len(chat.messages) > 0: 
               if chat.messages[0].sender_id == username or chat.messages[0].sender_id == username:
                    return chat
        return None





