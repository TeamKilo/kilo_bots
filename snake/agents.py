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


class SnakeGoForFruitAgent(SnakeBaseAgent):
    def __init__(self, username: str):
        self._username = username
        self._fruit = None

    def get_next_move(self, state: SnakeState):
        player_head = state.game_state["players"][self._username][0]
        if len(state.game_state['fruits']) == 0:
            return SnakeMove(random.choice(state.valid_moves(self._username)))
        else:
            if self._fruit is None or self._fruit not in state.game_state['fruits']:
                self._fruit = state.game_state['fruits'][0]
            directions = []
            if player_head['x'] < self._fruit['x']:
                directions.append('right')
            elif player_head['x'] > self._fruit['x']:
                directions.append('left')
            if player_head['y'] < self._fruit['y']:
                directions.append('up')
            elif player_head['y'] > self._fruit['y']:
                directions.append('down')
            return SnakeMove(random.choice(directions))
