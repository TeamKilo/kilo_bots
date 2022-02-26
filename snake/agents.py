import random

from snake.utils import SnakeState, SnakeMove


class SnakeBaseAgent:
    def get_next_move(self, state: SnakeState) -> SnakeMove:
        pass


class SnakeInteractiveAgent(SnakeBaseAgent):
    move_conversion_table = {
        "L": "left",
        "R": "right",
        "U": "up",
        "D": "down"
    }

    def get_next_move(self, state: SnakeState):
        move = input("Move (L/R/U/D): ")
        while move not in SnakeInteractiveAgent.move_conversion_table:
            move = input("Please enter a valid move")
        return SnakeMove(SnakeInteractiveAgent.move_conversion_table[move])


class SnakeRandomAgent(SnakeBaseAgent):
    def __init__(self, username: str):
        self._username = username

    def get_next_move(self, state: SnakeState):
        return SnakeMove(random.choice(state.valid_moves(self._username)))
