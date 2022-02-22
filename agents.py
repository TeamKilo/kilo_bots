from mcts import mcts
from utils import Connect4State, Connect4Move
import random


class Connect4BaseAgent:
    def get_next_move(self, state: Connect4State) -> Connect4Move: pass


class Connect4InteractiveAgent(Connect4BaseAgent):
    def get_next_move(self, state: Connect4State) -> Connect4Move:
        # Make Move
        move = input("Move (column number): ")
        while not state.validate_move(move):
            move = input("Please enter a valid move: ")
        return Connect4Move(int(move))


class Connect4RandomAgent(Connect4BaseAgent):
    def get_next_move(self, state: Connect4State) -> Connect4Move:
        valid_moves = []
        for i, row in enumerate(state.game_state['cells']):
            if len(row) < Connect4State.GAME_BOARD_HEIGHT:
                valid_moves.append(i)
        return Connect4Move(random.choice(valid_moves))


class Connect4MCTSAgent(Connect4BaseAgent):
    def __init__(self, username: str, timelimit: float, probabilistic: bool):
        self._username = username
        self._timelimit = timelimit
        self._probabilistic = probabilistic

    def get_next_move(self, state: Connect4State) -> Connect4Move:
        return Connect4Move(mcts(state.to_O_X(), state.symbol_player_map[self._username], self._timelimit, self._probabilistic))
