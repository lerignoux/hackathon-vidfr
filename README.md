# VidFr
A hackaton mini game backend project.


## tldr
```
docker run --name hackaton-vidfr-db -d mongo
docker run --name hackaton-vidfr --restart=always -p 1443:80 --link hackaton-vidfr-db:mongo -v ~/Projects/hackaton-vidfr/:/app -d jazzdd/alpine-flask
```

## Project:

The goal is to help foreigners get a grip on french difficult tricky mistakes related to the culture or environment.
You indeed not often learn these in the books.

The content is not publicly available, but feel free to reach us if you are interested

[Our presentation](/static/Presentation.pdf)
[Our business model](/static/BusinessModel.pdf)

This Hackaton was organised by the Alliance Francaise of Shanghai. Theme was French language and culture


## API:

Rest Json api

### POST /users{username}
-> user_id

#### errors:
403: username already exists

#### ex
```
{'user_id': '000', 'username': 'toto'}
```

### GET /user
-> name
-> list of battle history
  ->  player_score
  ->  oppponents
  ->  opponents scores

Get user details and his leaderboards (history)

#### errors:
404: User not found

#### ex:
```
{
    "username": "toto",
    "history": [
        {
          "title": "Social situation"
          "opponent_name_1": [0, 0, 1]
          "opponent__name_2": [1, 2, 1]
        }
    ]
}
```

### POST /game{user_id}
  ->   battle_tag
  ->   game_id
// Create a game

#### ex:
```
{'game_id': '000', 'battle_tag': '1234'}
```

### POST /game{user_id, battle_tag}
  -> game_id

join a game

#### errors:
404: game not found

#### ex:
```
{'game_id': '000', 'title':'content_tile'}
```

### GET /scene?game_id=000&user_id=000
-> video_name
-> choices
-> good {video_name, explanation}
-> bad {video_name, explanation}

Get next scene content

#### errors:
404: game already completed, no scene found

#### ex
```
{
    'content': 'firstSceneVideo.mp4',
    'choices': {'good': 'Une Demi', 'bad': "Un demi"},
    'good': {'content': "MyGoodAnswer.mp4", 'reason': "Yeah cheers to that"},
    'bad': {'content': "MyBadAnswre.mp4", 'reason': "You should know that, drink more"}
}
```

### POST /scene {user_id, game_id, choice='good'/'bad'}

Send user answer to this game

#### errors:
400: choice not acceptable (must be "good" or "bad")
404: no game found with this user

#### ex:
```
{}
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
