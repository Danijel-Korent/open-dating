import json
import sys


class DB: 
    def __init__(self, filename="mock_database.json"):
        with open("mock_database.json") as db:
            d = json.load(db)
            db.close()
            self.users = d['users']
            self.current_id = d['current_id']
            self.matches = d['matches']
            self.messages = d['messages']
            self.messages2 = d['messages2']

    def save(self):
        with open("mock_database.json","r+") as db:
            db.seek(0)
            db.truncate()
            new_db = dict(users = self.users, current_id=self.current_id, matches=self.matches,messages=self.messages,messages2=self.messages2)
            json.dump(new_db, db, indent=4)

    def get_user_by_id(self,id):
        for user in self.users:
            if str(user['id']) == str(id):
                return user
        
        return None


