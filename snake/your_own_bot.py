from snake.agents import SnakeBaseAgent
from snake.utils import SnakeState, SnakeMove


class SnakeUserDefinedAgent(SnakeBaseAgent):
    def __init__(self, username):
        self._username = username

    def get_next_move(self, state: SnakeState) -> SnakeMove:
        pass
