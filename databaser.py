from pymongo import MongoClient

import datetime

added_date = datetime.date.today()


def connect_db(db_name, db_pass):
    cluster = MongoClient(
        f"mongodb+srv://test4bot:{db_pass}@cluster0.4ibgi.mongodb.net/{db_name}?retryWrites=true&w=majority"
    )
    return cluster


class Users:
    
    def __init__(self, db_name, db_pass, collection):
        cluster = connect_db(db_name, db_pass)
        db = cluster[db_name]
        collection = db[collection]
        self.collection = collection

    def add_user(self, username, chat_id):
        if self.collection.find({"chat_id": chat_id}) is None:
            self.collection.insert_one({
                "name": username, 
                "chat_id": chat_id, 
                "date joined": datetime.date.today()
                }
            )
        else:
            pass

    def get_chat_id_of_all_users(self):
        return [users['chat_id'] for users in self.collection.find({})]

    def delete_user(self, chat_id):
        # Delete the user from the database, the user is represented
        # by the chat_id
        self.collection.delete_one({"chat_id": chat_id})
