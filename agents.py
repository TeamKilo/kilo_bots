from utils import Connect4State, Connect4Move
import random
import copy


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
    def get_next_move(self, state: Connect4State) -> Connect4Move:
        # TODO: implement
        pass
