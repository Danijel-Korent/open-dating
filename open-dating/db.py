import json
import sys
from typing import Dict
from dataclasses import dataclass, asdict
from enum import Enum

class Gender(Enum):
    MALE = 0
    FEMALE = 1
    OTHER = 2

    @staticmethod
    def from_str(gender_str: str):
        match gender_str.lower():
                case "male":
                    return Gender.MALE
                case "female":
                    return Gender.FEMALE
                case _:
                    return Gender.OTHER



@dataclass
class Preferences:
    gender: Gender
    age_max: int
    age_min: int
    distance_meters: int

@dataclass
class User:
    username: str
    name: str
    age: int
    gender: Gender
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
class Conversation:
    messages: list[Message]

@dataclass
class DB: 
    users: list[User]
    current_username: str
    matches: list[Match]
    messages: list[Conversation]

    def __init__(self, filename="mock_database.json"):
        self.filename=filename
        self.load() 

    def load(self):
        print("Loaded DB")
        with open(self.filename) as db:
            d = json.load(db)
            self.from_json(d)
            db.close()
    
    def from_json(self, json_dict: dict):
        for user in json_dict['users']:
            self.users.append(
                User(
                    username=user['username'], 
                    name=user['name'],
                    age=user['age'],
                    gender=Gender.from_str(user['gender']),
                    location=user['location'],
                    bio=user['bio'],
                    pictures=user['profile_pictures'],
                    preferences=Preferences(
                        gender=Gender.from_str(user['preferences']['gender']),
                        age_min=user['preferences']['age_range']['min'],
                        age_max=user['preferences']['age_range']['max'],
                        distance_meters=user['preferences']['location_range']
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

        self.messages = [
                Conversation(
                    messages=[
                        Message(
                            sender_id=msg['sender_id'],
                            receiver_id=msg['receiver_id'],
                            timestamp=msg['timestamp'],
                            message=msg['message']
                        )
                        for msg in conversation
                    ]
                )
                for conversation in json_dict['messages']
            ]

    def save(self):
        with open(self.filename,"r+") as db:
            db.seek(0)
            db.truncate()
            new_db = asdict(self)
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
        chats = self.messages
        matches = self.get_current_user_matches()  

        chats_final = []

        for match in matches:
            chat = self.get_user_chat(match['username'])
            if chat == None:
                chat = {}
            chats_final.append({"user": match, "chat": chat})


        return chats_final



    def get_user_chat(self, username):
        for chat in self.messages:
            if len(chat.messages) > 0: 
               if chat.messages[0].sender_id == username or chat.messages[0].sender_id == username:
                    return chat





