import clientlib.wrapper as wrapper


# TODO implement
class Connect4State(wrapper.GenericGameState):
    players = []
    state = "waiting"
    can_move = []
    winners = []
    game_name = "connect_4"
    game_state = {"cells": [], "winner": ""}

    def update_game_state(self, encoded_game_state: dict):
        self.players = encoded_game_state['players']
        self.state = encoded_game_state['state']
        self.can_move = encoded_game_state['can_move']
        self.winners = encoded_game_state['winners']
        self.game_state = encoded_game_state['game_state']

    def get_players(self):
        return self.players

    def get_state(self):
        return self.state

    def is_waiting_for_start(self):
        return self.state == "wait"


# TODO implement
class Connect4Move(wrapper.GenericGameMove):
    def encode_game_state(self):
        pass


if __name__ == '__main__':
    client = wrapper.GenericGameClient('connect_4')
    client.join_game("game_156684636527260407708829519575458565160", "theo")

