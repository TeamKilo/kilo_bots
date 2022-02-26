# Kilo Bots
This repo contains a client side library for the general API,
an example game state management class for a Connect 4 game and a Snake game, and 
a few example bots.

## Client side library: 
_clientlib/wrapper.py_

TODO

## Sample Bots: 
_\<game_type\>/agents.py_

TODO

- Random Agent
- Interactive Agent
- MCTS (UCT) Agent for Connect4

## Games supported
- Connect4
- Snake # TODO TEST

## Development

[Python3](https://www.python.org/) must be installed for development.

Run the program with
```shell
python main.py [-h] -t GAME_TYPE -a AGENT -u USERNAME [-g GAME_ID]
```
Note that if the `-g` argument isn't present, then a new game will be created.

## Technologies
- [Python](https://www.python.org/)

## Other Projects
- Frontend: [kilo_frontend](https://github.com/TeamKilo/kilo_frontend)
- Backend: [kilo_server](https://github.com/TeamKilo/kilo_server)

## Authors
- [Theo](https://github.com/MilkFansHelloWorld)

## License
This project is dual-licensed under both the MIT License and the Apache License (Version 2.0). See [LICENSE-APACHE](./LICENSE-APACHE) and [LICENSE-MIT](./LICENSE-MIT) for details.