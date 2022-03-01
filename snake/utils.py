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
    MIN_X = -100
    MIN_Y = -100
    MAX_X = 100
    MAX_Y = 100

    def __init__(self):
        super(SnakeState, self).__init__()

    def update_game_state(self, encoded_game_state: dict):
        super(SnakeState, self).update_game_state(encoded_game_state)

    def valid_moves(self, username: str):
        moves = []
        players = self.game_state["players"]
        if username in players:
            if players[username][0]["x"] < SnakeState.MAX_X:
                moves.append("right")
            if players[username][0]["x"] > SnakeState.MIN_X:
                moves.append("left")
            if players[username][0]["y"] > SnakeState.MIN_Y:
                moves.append("down")
            if players[username][0]["y"] < SnakeState.MAX_Y:
                moves.append("up")
        return moves
