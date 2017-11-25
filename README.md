# hackathon_ff
A hackathon mini game backend project


## tldr
```
docker run --name hackathon-ff-db -d mongo
docker run --name hackathon-ff --restart=always -p 1443:80 --link hackathon-ff-db:mongo -v ~/Projects/hackathon-ff/:/app -d jazzdd/alpine-flask
```

## API:

Rest Json api

### GET /user
-> name
-> list of battle history
    player_id
    player_score
    oppponent
    opponent score
// get user with leaderboards

ex:
```
{
    'code': 200,
    'data': {
        'username': 'toto',
        'history': [{
            'game_id': '0',
            'player': {'score': 3},
            'opponent': {'score': 1}
        }]
    }
}
```

### POST /game
  ->   battle_tag
  ->   game_id
// Create a game

ex:
```
'code': 200, data: {'game_id': '000', 'battle_tag': '1234'}}
```

POST /game{battle_tag}
  -> game_id
//join a game

ex:
```
{'code': 200, 'data': {'game_id': '000'}}
```

### GET /scene{game_id, user_id}
-> video_name
-> choices
-> good {video_name, explanation}
-> bad {video_name, explanation}
// Get next scene content

ex
```
{
    'code': 200,
    'data': {
        'content': 'firstSceneVideo.mp4',
        'choices': {'good': 'Une Demi', 'bad': "Un demi"},
        'good': {'content': "MyGoodAnswer.mp4", 'reason': "Yeah cheers to that"},
        'bad': {'content': "MyBadAnswre.mp4", 'reason': "You should know that, drink more"}
    }
}
```

### POST /scene {user_id, choice='good'/'bad'}
// Send user answer to this

ex:
```
{'code': 200}
```
