import logging
import pymongo
from bson import ObjectId

from pymongo import MongoClient

log = logging.getLogger("hackaton-vidfr")


class UserHandler(object):

    def __init__(self):
        client = MongoClient('mongo', 27017)
        self.db = client.hackathon_ff
        self.user = self.db.user

    def init_db(self):
        self.db.user.create_index([('username', pymongo.ASCENDING)], unique=True)

    def get_user(self, user_id):
        return self.user.find_one({'_id': ObjectId(user_id)})

    def add_user(self, username, password=None):
        entry = {
            "username": username,
        }
        if password is not None:
            entry['password'] = password
        return self.user.find_one({'_id': self.user.insert_one(entry).inserted_id})

    def log_user(self, username, password):
        user = self.user.find_one({'username': username})
        log.info(password)
        log.info(user.get('password'))
        if user.get('password') is None:
            return user
        if str(user['password']) == str(password):
            return user
        else:
            raise Exception("invalid password")

    @classmethod
    def to_dict(cls, user):
        log.info(user)
        user_id = user['_id']
        return {
            'user_id': str(user_id),
            'username': user['username']
        }
