# hackathon_ff
A hackathon mini game backend project

## API:

Rest Json api

GET /user
-> name
-> list of battle history
    player_id
    player_score
    oppponent
    opponent score
// get user with leaderboards

POST /game
  ->   battle_tag
  ->   game_id
// Create a game

POST /game{battle_tag}
  -> game_id
//join a game

GET /scene{game__id, user_id}
-> video_name
-> choices
-> good {video_name, explanation}
-> bad {video_name, explanation}
// Get next scene content


-> POST /scene {user_id, choice='good'/'bad'}
// Send user answer to this
