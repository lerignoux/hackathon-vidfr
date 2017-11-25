import json
import logging
import pymongo
import random

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

    def get_user_history(self, user_id):
        """
        returns the user history to avoid replaying the same games
        """
        games = self.game.find({'users.user_id': user_id}, {})
        return list(games)

    def new_game(self, user_id):
        content = ContentHandler().get_content(played=self.get_user_history(user_id))
        battle_tag = "%s#%d" % (UserHandler().get_user(user_id)['username'], random.randint(1111, 9999))
        entry = {
            'battle_tag': battle_tag,
            'content_id': content['_id'],
            'users': {user_id: {'result': []}},
            'status': 'requested'
        }
        result = self.game.find_one({'_id': self.game.insert_one(entry).inserted_id})
        result['title'] = content['title']
        log.info(result)
        return result

    def join_game(self, user_id, battle_tag):
        game_id = self.game.find_one({'battle_tag': battle_tag})['_id']
        self.game.update_one(
            {'_id': game_id},
            {'$set': {'users.%s' % user_id: {'result': []}}},
            upsert=False
        )
        return self.game.find_one({'_id': game_id})

    def get_scene(self, user_id, game_id):
        game = self.game.find_one({'_id': ObjectId(game_id)})
        log.info(game)
        scene_id = len(game['users'][user_id]['result'])
        return ContentHandler().get_content_scene(game['content_id'], scene_id)

    def update_user_answer(self, user_id, game_id, answer):
        if answer not in [0, 1]:
            raise BadAnswerException("only %s answers are accepted" % [0, 1])
        game = self.game.find_one({'_id': ObjectId(game_id)})
        if len(game['users'][user_id]['result']) >= self.config.get('scenes', 3):
            raise GameEndedException("All scenes answered already by user %s" % user_id)

        self.game.update_one(
            {'_id': ObjectId(game_id)},
            {'$push': {'users.%s.result' % user_id: answer}},
            upsert=False
        )

    def get_player_history(self, user_id):
        history = []
        key = "users.%s" % user_id
        games = self.game.find({key: {'$exists': 1}})
        for game in games:
            content = ContentHandler().get_content(content_id=game['content_id'])
            res = {'score': [], 'opponents': {}, 'title': content['title']}
            for key in game['users']:
                if user_id == key:
                    res['score'] = game['users'][key]['result']
                else:
                    name = UserHandler().get_user(key)['username']
                    res['opponents'][name] = game['users'][key]['result']
            if len(res['score']) > 0 or len(res['opponents'].keys()) > 1:
                history.append(res)
        return history

    @classmethod
    def to_dict(cls, game):
        res = {
            'game_id': str(game['_id']),
            'battle_tag': game['battle_tag']
        }
        if 'title' in game:
            res['title'] = game['title']
        return res
