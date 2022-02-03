import requests
import os

BASE_URL = os.environ[
    'GAME_SERVER_BASE_URL'] if 'GAME_SERVER_BASE_URL' in os.environ else "https://team-kilo-server.herokuapp.com"


class GenericGameState:
    def update_game_state(self, encoded_game_state: dict):
        """
        Update the game state stored in the object given a dict
        :return: ()
        """
        pass


class GenericGameMove:
    def encode_game_state(self):
        """
        Convert the move to a dict/JSON-like format
        :return:
        """
        pass


class GenericGameClient():
    def __init__(self, game_type):
        self.game_type = game_type
        self.username = ""
        self.game_id = ""
        self.game_state = None
        self.session_id = ""

    # Create game
    def create_game(self):
        pass

    def join_game(self, username: str):
        pass

    def get_state_and_update(self, current_state: GenericGameState) -> dict:
        pass

    def submit_move(self, move: GenericGameMove):
        pass

    def wait_for_update(self) -> bool:
        pass
