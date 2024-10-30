import json
import sys


class DB: 
    def __init__(self, filename="mock_database.json"):
        self.filename=filename
        self.load() 

    def load(self):
        print("Loaded DB")
        with open(self.filename) as db:
            d = json.load(db)
            db.close()
            self.users = d['users']
            self.current_username = d['current_username']
            self.matches = d['matches']
            self.messages = d['messages']
            self.messages2 = d['messages2']


    def save(self):
        with open("mock_database.json","r+") as db:
            db.seek(0)
            db.truncate()
            new_db = dict(users = self.users, current_username=self.current_username, matches=self.matches,messages=self.messages,messages2=self.messages2)
            json.dump(new_db, db, indent=4)

    def get_user_by_username(self,username):
        for user in self.users:
            if str(user['username']) == username:
                return user
        
        return None

    def get_current_user_matches(self):
        matches = []
        for match in self.matches:
            if match['user1'] == self.current_username:
                matches.append(self.get_user_by_username(match['user2']))
            if match['user2'] == self.current_username:
                matches.append(self.get_user_by_username(match['user1']))


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
            if len(chat) > 0: 
               if chat[0]['sender_id'] == username or chat[0]['receiver_id'] == username:
                    return chat





