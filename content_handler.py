import logging
from bson import ObjectId

from pymongo import MongoClient

log = logging.getLogger("hackaton-vidfr")

DEFAULT_CONTENT = {
    'title': "default",
    'scenes': [{
        'content': 'firstSceneVideo.mp4',
        'choices': {'good': 'Une Demi', 'bad': "Un demi"},
        'good': {'content': "MyGoodAnswer.mp4", 'reason': "Yeah cheers to that"},
        'bad': {'content': "MyBadAnswre.mp4", 'reason': "You should know that, drink more"}
    }]
}


class ContentHandler(object):

    def __init__(self):
        client = MongoClient('mongo', 27017)
        self.db = client.hackathon_ff
        self.content = self.db.content

    def add_content(self, data):
        log.debug("Adding content %s" % data)
        entry = data or DEFAULT_CONTENT
        result = self.content.find_one({'_id': self.content.insert_one(entry).inserted_id})
        return result == 1

    def get_content(self, played=[]):
        content = self.content.find_one({'_id': {"$nin": played}}, {'_id': 0})
        if not content:
            content = self.content.find_one({}, {'_id': 0})
        return content

    def get_content_scene(self, content_id, scene):
        content = self.content.find_one({'_id': content_id}, {'_id': 0})
        return content.scenes[scene]

    def get_all(self):
        return list(self.content.find())

    def update_content(self, content_id, data):
        log.info("updating %s, query=%s" % (content_id, {'$set': data}))
        self.content.update_one({'_id': ObjectId(content_id)}, {'$set': data})
