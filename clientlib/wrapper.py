import requests
import os

BASE_URL = os.environ[
    'GAME_SERVER_BASE_URL'] if 'GAME_SERVER_BASE_URL' in os.environ else "https://team-kilo-server.herokuapp.com"


class ClientLibBaseException(Exception):
    pass


class ClientLibRequestException(ClientLibBaseException):
    def __init__(self, message, status=None):
        self.status = status
        super(ClientLibRequestException, self).__init__(message)


class ClientLibInternalException(ClientLibBaseException):
    def __init__(self, message):
        super(ClientLibInternalException, self).__init__(message)


class GenericGameState:
    def __init__(self):
        """
        Player agnostic representation of the game state
        """
        self.players = []
        self.stage = "waiting"  # waiting | in_progress | ended
        self.can_move = []
        self.winners = []
        self.game_state = {}

    def __str__(self):
        return '''
-----------------
STATE OF GAME: {}
players: {}
can_move: {}
winner: {}
game-specific state:
{}
'''.format(self.stage, self.players, self.can_move, self.winners, self.game_state)

    def update_game_state(self, encoded_game_state: dict):
        """
        Update the game state stored in the object given a dict
        :return: ()
        """
        self.players = encoded_game_state['players']
        self.stage = encoded_game_state['stage']
        self.can_move = encoded_game_state['can_move']
        self.winners = encoded_game_state['winners']
        self.game_state = encoded_game_state['payload']

    def is_waiting_for_start(self) -> bool:
        return self.stage == "waiting"

    def is_ended(self) -> bool:
        return self.stage == "ended"

    def is_in_progress(self) -> bool:
        return self.stage == "in_progress"

    def player_can_move(self, username_) -> bool:
        return username_ in self.can_move

    def has_won(self, username_) -> bool:
        return self.is_ended() and username_ in self.winners


class GenericGameMove:
    """ Representation of a move to facilitate parsing """
    def encode_game_move(self):
        """
        Convert the move to a dict/JSON-like format
        :return:
        """
        pass


class GenericGameClient:
    def __init__(self, game_type, game_id=None, username=None):
        self.game_type = game_type
        self.username = username
        self.game_id = game_id
        self.game_state = None
        self.session_id = ""
        self.clock = 0

    # Create game
    @staticmethod
    def create_game(game_type):
        res = requests.post("{}/api/create-game".format(BASE_URL), json={"game_type": game_type})
        if res.ok:
            res_json = res.json()
            if res_json['game_id'] != "":
                return res_json['game_id']
            else:
                raise ClientLibRequestException("No Game Id Returned")
        else:
            raise ClientLibRequestException(res.reason, res.status_code)

    def join_game(self, game_id: str = None, username: str = None):
        if username is not None:
            self.username = username
        if game_id is not None:
            self.game_id = game_id
        res = requests.post("{}/api/{}/join-game".format(BASE_URL, self.game_id),
                            json={"username": self.username})
        if res.ok:
            res_json = res.json()
            if res_json['session_id'] != "":
                self.session_id = res_json['session_id']
            else:
                raise ClientLibRequestException("No Session Id Returned")
        else:
            raise ClientLibRequestException(res.reason, res.status_code)

    def get_state(self) -> dict:
        """ get state and return it as a dictionary """
        if self.game_id is None:
            raise ClientLibInternalException("No Game Id provided, you need to call create game or construct a client "
                                             "with a game id")
        res = requests.get("{}/api/{}/get-state".format(BASE_URL, self.game_id))
        if res.ok:
            res_json = res.json()
            return res_json
        else:
            raise ClientLibRequestException(res.reason, res.status_code)

    def update_state(self, current_state: GenericGameState) -> ():
        """ get state and update the state object """
        current_state.update_game_state(self.get_state())

    def submit_move(self, move: GenericGameMove):
        if self.game_id is None:
            raise ClientLibInternalException("No Game Id provided, you need to call create game or construct a client "
                                             "with a game id")
        if self.session_id is None:
            raise ClientLibInternalException("No Session Id provided. Please call join_game to join a game first.")
        res = requests.post("{}/api/{}/submit-move".format(BASE_URL, self.game_id),
                            json={"session_id": self.session_id, "payload": move.encode_game_move()})
        if res.ok:
            res_json = res.json()
            if not res_json["success"]:
                raise ClientLibRequestException("Update failed")
            else:
                return
        else:
            raise ClientLibRequestException(res.reason, res.status_code)

    def wait_for_update(self) -> bool:
        """ Blocks and waits for server to respond.
        Returns true when SOME update has happened, false if timeout (5 seconds)"""
        try:
            res = requests.get("{}/api/{}/wait-for-update".format(BASE_URL, self.game_id), params={"since": self.clock})
        except requests.exceptions.Timeout as e:
            return False
        if res is not None:
            if res.ok:
                res_json = res.json()
                clk = int(res_json["clock"])
                if clk > self.clock:
                    self.clock = clk
                    return True
                return False
            else:
                raise ClientLibRequestException(res.reason, res.status_code)
        return False
