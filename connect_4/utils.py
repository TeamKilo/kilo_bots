import copy

import clientlib.wrapper as wrapper


# Here we assume the format of move being just an integer
class Connect4Move(wrapper.GenericGameMove):
    """ GameMove class for the Connect4 game """

    def __init__(self, move_: int):
        # TODO maybe add validation here
        self.move = move_

    def encode_game_move(self):
        return {
            "game_type": "connect_4",
            "column": self.move
        }


class Connect4State(wrapper.GenericGameState):
    """ GameState class for the Connect4 game """
    GAME_BOARD_HEIGHT = 6
    GAME_BOARD_WIDTH = 7

    def __init__(self):
        super(Connect4State, self).__init__()
        self.symbol_player_map = {}

    def update_game_state(self, encoded_game_state: dict):
        super(Connect4State, self).update_game_state(encoded_game_state)
        if len(self.symbol_player_map) == 0 and len(self.players) == 2:
            # Game has just got enough players: update symbol player map for consistency in the to_O_X method
            self.symbol_player_map[self.players[0]] = 'O'
            self.symbol_player_map[self.players[1]] = 'X'

    def validate_move(self, move_) -> bool:
        if isinstance(move_, Connect4Move):
            move_ = move_.move
        return 0 <= int(move_) < len(self.game_state['cells'])

    def to_O_X(self):
        ret = list(map(lambda col: list(map(lambda el: self.symbol_player_map[el], col)), self.game_state['cells']))
        return ret

    def print_state(self):
        res = ""
        for col in self.game_state["cells"]:
            for row in col:
                res += "|"
                res += self.symbol_player_map[row]
            res += "|\n"
            for _ in range(len(col) * 2 + 1):
                res += "-"
            res += "\n"
        return res

    def __str__(self):
        return '''
------------------
STATE OF GAME: {}
players: {}, mapped to [O, X] respectively
can_move: {}
winner: {}
GAME BOARD
{}
------------------
'''.format(self.stage, self.players, self.can_move, self.winners, self.print_state())
