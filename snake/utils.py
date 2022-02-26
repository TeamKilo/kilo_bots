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
    GAME_BOARD_HEIGHT = 100
    GAME_BOARD_WIDTH = 100

    def __init__(self):
        super(SnakeState, self).__init__()

    def update_game_state(self, encoded_game_state: dict):
        super(SnakeState, self).update_game_state(encoded_game_state)

    def valid_moves(self, username: str):
        moves = []
        players = self.game_state["players"]
        if username in players:
            if players[username][0]["x"] < SnakeState.GAME_BOARD_WIDTH:
                moves.append("right")
            if players[username][0]["x"] > 0:
                moves.append("left")
            if players[username][0]["y"] > 0:
                moves.append("up")
            if players[username][0]["y"] < SnakeState.GAME_BOARD_HEIGHT:
                moves.append("down")
        return moves
