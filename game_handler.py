import json
import logging
import pymongo

from bson import ObjectId
from pymongo import MongoClient

from user_handler import UserHandler
from content_handler import ContentHandler

log = logging.getLogger("hackaton-vidfr")


class BadAnswerException(Exception):
    pass


class GameEndedException(Exception):
    pass


class GameHandler(object):

    Choices = ['good', 'bad']
    ContentScenes = 3

    def __init__(self):
        client = MongoClient('mongo', 27017)
        self.db = client.hackathon_ff
        self.game = self.db.game
        self.load_config()

    def load_config(self, config='config.json'):
        with open(config, 'r') as f:
            self.config = json.load(f).get('content')

    def init_db(self):
        self.db.game.create_index([('users.user_id', pymongo.ASCENDING), ('status', pymongo.ASCENDING)])
        self.db.game.create_index([('battle_tag', pymongo.ASCENDING)])

    def get_user_scene(self, user_id, game_id):
        return self.game.find_one({'user_id': user_id}, {})

    def get_user_history(self, user_id):
        """
        returns the user history to avoid replaying the same games
        """
        games = self.game.find({'users.user_id': user_id}, {})
        return list(games)

    def new_game(self, user_id):
        entry = {
            'battle_tag': UserHandler().get_user(user_id)['username'],
            'content_id': ContentHandler().get_content(played=self.get_user_history(user_id)),
            'users': {user_id: {'result': []}},
            'status': 'requested'
        }
        return self.game.find_one({'_id': self.game.insert_one(entry).inserted_id})

    def join_game(self, user_id, battle_tag):
        game_id = self.game.find_one({'battle_tag': battle_tag})._id
        self.game.update_one(
            {'_id': game_id},
            {'users.%s' % user_id: {'$set': {'result': []}}},
            upsert=False
        )
        return self.game.find_one({'_id': game_id})

    def get_scene(self, user_id, game_id):
        game = self.game.find_one({'_id': ObjectId(game_id)})

        for user in game.users:
            if user.user_id == user_id:
                scene_id = game[user_id].result.length()
        return ContentHandler.get_content_scene(game.content_id, scene_id)

    def update_user_answer(self, user_id, game_id, answer):
        if answer not in self.Choices.keys():
            raise BadAnswerException("only %s answers are accepted" % self.Choices.keys())
        game = self.game.find_one({'_id': ObjectId(user_id)})
        if game[user_id].result.length() > self.config.scenes:
            raise GameEndedException("All scenes answered already by user %s" % user_id)

        self.game.update_one(
            {'_id': ObjectId(game_id)},
            {'users.%s.result' % user_id: {'$push': answer}},
            upsert=False
        )

    @classmethod
    def to_dict(cls, game):
        return {
            'game_id': str(game['_id']),
            'battle_tag': game['battle_tag']
        }
