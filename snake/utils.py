import clientlib.wrapper as wrapper


class SnakeMoveValidationError(Exception):
    def __init__(self, move_):
        self.move = move_


class SnakeMove(wrapper.GenericGameMove):
    def __init__(self, move_: str):
        if move_ not in ["left", "right", "up", "down"]:
            raise SnakeMoveValidationError(move_)
        self.move = move_

    def encode_game_move(self):
        return {
            "game_type": "snake",
            "direction": self.move
        }


class SnakeState(wrapper.GenericGameState):

    def __init__(self):
        super(SnakeState, self).__init__()
        self.world_min = None
        self.world_max = None

    def update_game_state(self, encoded_game_state: dict):
        super(SnakeState, self).update_game_state(encoded_game_state)
        self.world_min = self.game_state['world_min']
        self.world_max = self.game_state['world_max']

    def valid_moves(self, username: str):
        moves = []
        players = self.game_state["players"]
        if username in players:
            if players[username][0]["x"] < self.world_max['x']:
                moves.append("right")
            if players[username][0]["x"] > self.world_min['x']:
                moves.append("left")
            if players[username][0]["y"] > self.world_min['y']:
                moves.append("down")
            if players[username][0]["y"] < self.world_max['x']:
                moves.append("up")
        return moves
