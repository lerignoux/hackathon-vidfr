# hackathon_ff
A hackathon mini game backend project


## tldr
```
docker run --name hackathon-ff-db -d mongo
docker run --name hackathon-ff --restart=always -p 1443:80 --link hackathon-ff-db:mongo -v ~/Projects/hackathon-ff/:/app -d jazzdd/alpine-flask
```

## API:

Rest Json api

### POST /users{username}
-> user_id

#### errors:
403: username already exists

#### ex
```
{'code': 200, 'data': {'user_id': '000', 'username': 'toto'}}
```

### GET /user
-> name
-> list of battle history
    player_id
    player_score
    oppponent
    opponent score
// get user with leaderboards

#### errors:
404: User not found

#### ex:
```
{
    'code': 200,
    'data': {
        'username': 'toto',
        'history': [{
            'game_id': '0',
            'player': {'result': [0, 0, 1]},
            'opponent': {'result': [1, 1, 0]}
        }]
    }
}
```

### POST /game{user_id}
  ->   battle_tag
  ->   game_id
// Create a game

#### ex:
```
'code': 200, data: {'game_id': '000', 'battle_tag': '1234'}}
```

### POST /game{battle_tag}
  -> game_id
//join a game

#### errors:
404: game not found

#### ex:
```
{'code': 200, 'data': {'game_id': '000'}}
```

### GET /scene{game_id, user_id}
-> video_name
-> choices
-> good {video_name, explanation}
-> bad {video_name, explanation}
// Get next scene content

#### errors:
404: game already completed, no scene found

#### ex
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

### POST /scene {user_id, game_id, choice='good'/'bad'}
// Send user answer to this game

#### errors:
400: choice not acceptable (must be "good" or "bad")
404: no game found with this user

#### ex:
```
{'code': 200}
```

## Misc:
Setup commands:

### get users:
```
curl -XGET localhost:1443/user
```

### create a user:
```
curl -i -XPOST localhost:1443/user -H'Content-Type: ApplicationJson' -d'{"username": "toto"}'
```
