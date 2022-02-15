from utils import Connect4State, Connect4Move
from clientlib.wrapper import GenericGameClient
import random


class Connect4InteractiveAgent:
    def make_move(self, state: Connect4State, client: GenericGameClient) -> Connect4Move:
        # Make Move
        move = input("Move (column number): ")
        while not state.validate_move(move):
            move = input("Please enter a valid move: ")
        return Connect4Move(int(move))


class Connect4RandomAgent:
    def make_move(self, state: Connect4State, client: GenericGameClient) -> Connect4Move:
        valid_moves = []
        for i, row in enumerate(state.game_state['cells']):
            if len(row) < Connect4State.GAME_BOARD_HEIGHT:
                valid_moves.append(i)
        return Connect4Move(random.choice(valid_moves))
