
import argparse
import json
import logging
# from http://flask.pocoo.org/ tutorial
from flask import Flask, render_template, request, jsonify
from pymongo.errors import DuplicateKeyError

from content_handler import ContentHandler
from game_handler import GameHandler, BadAnswerException, GameEndedException
from user_handler import UserHandler


log = logging.getLogger("hackaton-vidfr")

parser = argparse.ArgumentParser(description='Show transversal xml properties.')
parser.add_argument('--debug', '-d', dest='debug',
                    action='store_true',
                    help='Debug mode')

app = Flask(__name__)
app.secret_key = "test"

GameHandler().init_db()
UserHandler().init_db()


class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.before_first_request
def initialize():
    logger = logging.getLogger("hackaton-vidfr")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        """%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n%(message)s"""
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')


@app.route('/user', methods=['POST'])
def new_user():
    """
    create a user
    """
    data = json.loads(request.data)
    username = data.get('username')
    try:
        user = UserHandler().add_user(username)
    except DuplicateKeyError as e:
        raise InvalidUsage(str(e), status_code=403)

    return json.dumps(UserHandler.to_dict(user))


@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('user_id')
    user = UserHandler().get_user(user_id)
    if not user:
        raise InvalidUsage("User %s not found" % user_id, status_code=404)

    return json.dumps(UserHandler.to_dict(user))


@app.route('/game', methods=['POST'])
def game():
    """
    create or join a game
    """
    data = json.loads(request.data)
    battle_tag = data.get('battle_tag')
    user_id = data.get('user_id')
    if user_id is None:
        raise InvalidUsage("user_id required", status_code=401)
    if battle_tag is not None:
        game = GameHandler().join_game(user_id, battle_tag)
        return json.dumps(GameHandler.to_dict(game))
    else:
        game = GameHandler().new_game(user_id)
        return json.dumps(GameHandler.to_dict(game))


@app.route('/scene', methods=['GET'])
def get_scene():
    user_id = request.args.get('user_id')
    game_id = request.args.get('game_id')
    GameHandler().get_user_scene(user_id, game_id)
    return json.dumps({
        'content': 'firstSceneVideo.mp4',
        'choices': {'good': 'Une Demi', 'bad': "Un demi"},
        'good': {'content': "MyGoodAnswer.mp4", 'reason': "Yeah cheers to that"},
        'bad': {'content': "MyBadAnswre.mp4", 'reason': "You should know that, drink more"}
    })


@app.route('/scene', methods=['POST'])
def post_scene():
    """
    Send user choice on this scene
    """
    data = json.loads(request.data)
    user_id = data.get('user_id')
    game_id = data.get('game_id')
    choice = data.get('Choice')
    try:
        GameHandler().update_user_answer(user_id, game_id, choice)
    except BadAnswerException as e:
        raise InvalidUsage(str(e), status_code=400)
    except GameEndedException as e:
        raise InvalidUsage(str(e), status_code=404)
    return json.dumps({})


@app.route('/content', methods=['GET'])
def get_all_content():
    content = ContentHandler().get_all()
    for cont in content:
        cont['_id'] = str(cont['_id'])
    return json.dumps(content)


@app.route('/content', methods=['POST'])
def add_content():
    """
    Send user choice on this scene

    Data expected:
    'title': "default",
    'scenes':{
        'content': 'firstSceneVideo.mp4',
        'choices': {'good': 'Une Demi', 'bad': "Un demi"},
        'good': {'content': "MyGoodAnswer.mp4", 'reason': "Yeah cheers to that"},
        'bad': {'content': "MyBadAnswre.mp4", 'reason': "You should know that, drink more"}
    }
    """
    data = json.loads(request.data)
    password = data.get('password')

    with open('config.json', 'r') as f:
        if password != json.load(f).get('admin', {}).get('password', ''):
            raise InvalidUsage("Passord credentials required", status_code=401)

    data = data['content']
    content = {
        'title': data['title'],
        'scenes': [{
            'content': scene['content'],
            'choices': scene['choices'],
            'good': scene['good'],
            'bad': scene['bad']
        } for scene in data['scenes']]
    }
    content_id = data.get('_id')
    if content_id:
        log.debug("updating content %s" % content_id)
        ContentHandler().update_content(content_id, content)
    else:
        log.debug("New content")
        ContentHandler().add_content(content)
    return json.dumps({})


if __name__ == "__main__":
    args = parser.parse_args()

    app.run()
