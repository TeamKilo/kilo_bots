from .utils import Connect4State, Connect4Move
from .agents import Connect4BaseAgent


class Connect4UserDefinedAgent(Connect4BaseAgent):
    def __init__(self, username):
        self._username = username

    def get_next_move(self, state: Connect4State) -> Connect4Move:
        # TODO: IMPLEMENT
        pass
