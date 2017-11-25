import logging
import pymongo

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
        return self.user.find_one({'user_id': user_id})

    def add_user(self, username):
        entry = {
            "username": username,
        }
        return self.user.find_one({'_id': self.user.insert_one(entry).inserted_id})

    @classmethod
    def to_dict(cls, user):
        log.info(user)
        user_id = user['_id']
        return {
            'user_id': str(user_id),
            'username': user['username']
        }
