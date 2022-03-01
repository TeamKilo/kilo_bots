# Docs & Tutorial

This document presents an overview of how to use/create bots for our
game server with this repository. It will include a brief overview of the system,
the workflow for each game presented by the API and how to use the front-end. It will also 
contain a tutorial of creating a bot using the code/libraries presented in this repo.

## A few things before we start

Before you start trying to create a bot, there are a few things you might want to know. If you just 
want to know how to implement a bot, please jump to the tutorial.

### What games to we support

We only support, in general, turn-based, discrete time, fixed player count multiplayer games 
for now. The two games we've implemented are Connect 4 and a turn-based multiplayer Snake. This has had 
an impact on how we designed our API, as presented in the section below.

### Back End: the API

Our API is hosted at https://team-kilo-server.herokuapp.com/api. API docs can be viewed [here](https://kilo-games.netlify.app/docs).

More details on the backend and how to communicate with the API in the Advanced section below.
However, this is not needed to understand how to create a bot, for we have a client side library that 
wraps around it sufficiently so that you don't need to worry about this.

### Front End: how to use it

The [front-end](https://kilo-games.netlify.app/) gives means to:
- Create a game
- Spectate a game
- Play a game manually

It also contains the API docs for our server.

It is rather straightforward to use so we won't include details here.

## Creating a bot for connect 4

TODO

### Step 1: SETUP

#### The client side library

#### The bots available

#### How to run the bots

### Step 2: Creating your own bot

#### Before we start: the GameState object and the GameMove object

#### Implementing [your_own_bot.py](/connect_4/your_own_bot.py)

## Advanced

### Implementing support for a new game

### Implementing your own client -- API Workflow: how to communicate with the server

This section will contain an overview of the communication workflow between 
client and server in our system.

The overall workflow is basically: we create a game, join the game by game_id to get a session id, and play the game by authenticating 
with the session_id. To listen to updates, the client repeatedly polls the `wait-for-update` route of the server, which blocks until it hears 
any new updates, or returns immediately if there has been updates since the last time the client updated its local state.

#### Creating a game

A game is created by sending a POST request to `/create-game` with the type of 
game you want to create. As a response, the server will give you a `game_id`, a 
unique identifier of the game. This `game_id` is very important, as it will serve as a handle to 
the game on the server side.

This step is GAME AGNOSTIC, i.e. it doesn't depend on the game.

How do you know when the game starts? This will be covered in a later section.

#### Joining a game

After a game is created, other players can join the game by sending a POST request to `/{game_id}/join_game` with a 
username. The game will start when enough players have join the game. 

When joining a game, the server will return a session_id, which is to be safely kept as it will be used 
as a means of authenticating a player in a game. 

This step is also game agnostic.

#### Playing a game

From the moment when the game has started, one can ask the server for the state of the game at `GET /{game_id}/get-state`.
The request would return you a JSON object resembling to the following:

```json
{
  "players": [
    "player1",
    "player2"
  ], // The players in the game
  "stage": "in_progress",
  "last_updated": "[SOME TIMESTAMP]",
  "can_move": [
    "player1"
  ], // Who's turn it is to play
  "winners": [],
  "payload": {
    "game_type": "connect_4",
    "cells": [[]] // AN ARRAY OF CONNECT 4 COLUMNS
  }
}
```

This object contains all the information you need for the state of the game. Two things are to be noted here:
- We have a `stage` field. This field can have value either `waiting`, `in_progress` or `ended`. One can 
only submit moves to the game when the stage is `in_progress`. 
- We have a `payload` field containing a JSON object. Everything in the response 
object is game agnostic except this field. The object this field contains is a **game-specific**
object that contains the state of the actual game board.

If it is your turn to play, you can then submit a move with your session id by sending a `POST /{game-id}/submit-move` request,
with the session_id AND a `payload` object in the body. The payload object is also **game-specific**, because it is an encoding 
of the move you want to submit to the game.

How do you know when it's your turn to play? This will be covered in a later section.

#### End of game

The game ends when the server thinks that the game has ended. In this case, 
when we send a get-state request, we'd get an object with `stage: ended`.

#### Now this is all good, but how does one know when there is an update in the game state?

This is arguably the one thing you would need to know to be able to write a bot from scratch.

Everytime you want to get the new state of the game, to see if there are any updates, you could just poll the server 
by repeatedly sending a get-state request. This, however, is very inefficient. Instead, you should poll a `GET /{game_id}/wait-for-update` 
route, which returns `updated: true` if there has been an update, `false` otherwise. If sent without parameters, we 
would block for 5 seconds waiting for an update, and if no update has happened, the server returns false, and we can poll again. Otherwise, there has 
been an update, and so you can send a `GET /{game_id}/get-state` request to get the new state.

To avoid missed updates, we extend this polling system with a clock-based synchronisation mechanism. 
Each client maintains with itself a clock, initialised at 0. This clock is a counter of how many updates/events have been recorded
by this client. The server, on its side, also maintains a clock number corresponding to the number of state updates that happened in the game. 
Update here means any change to the game state: someone joined the game, someone submitted a move, game has started, game has ended...

Each time we send a `wait-for-update` request, we pass the clock in as a parameter. If our clock 
is equal or bigger to that of the server, it means that there hasn't been an update in the game state since the last time we requested the 
games state. In this case, the server blocks for at most 5 seconds waiting for an update. If that happens, the server returns
`updated:true`, else `false`. Otherwise, the server responds immediately with `updated: true` so that the client can 
get the state again and proceed.

#### Overall workflow

TODO IMAGE DIAGRAM



