import clientlib.wrapper as wrapper


# Here we assume the format of move being just an integer
class Connect4Move(wrapper.GenericGameMove):
    def __init__(self, move_: int):
        # TODO maybe add validation here
        self.move = move_

    def encode_game_move(self):
        return {
            "column": self.move
        }


class Connect4State(wrapper.GenericGameState):
    GAME_BOARD_HEIGHT = 6
    GAME_BOARD_WIDTH = 7

    def __init__(self):
        self.players = []
        self.state = "waiting"  # waiting | in_progress | ended
        self.can_move = []
        self.winners = []
        self.game_name = "connect_4"
        self.game_state = {"cells": [], "winner": ""}

    def update_game_state(self, encoded_game_state: dict):
        self.players = encoded_game_state['players']
        self.state = encoded_game_state['state']
        self.can_move = encoded_game_state['can_move']
        self.winners = encoded_game_state['winners']
        self.game_state = encoded_game_state['payload']

    def get_players(self):
        return self.players

    def get_state(self):
        return self.state

    def is_waiting_for_start(self) -> bool:
        return self.state == "waiting"

    def is_ended(self) -> bool:
        return self.state == "ended"

    def is_in_progress(self) -> bool:
        return self.state == "in_progress"

    def player_can_move(self, username_) -> bool:
        return username_ in self.can_move

    def validate_move(self, move_) -> bool:
        if isinstance(move_, Connect4Move):
            move_ = move_.move
        return 0 <= int(move_) < len(self.game_state['cells'])

    def has_won(self, username_) -> bool:
        return self.is_ended() and username_ in self.winners


class Connect4Agent:
    def make_move(self, state: Connect4State, client: wrapper.GenericGameClient) -> Connect4Move:
        # Make Move
        move = input("Move (column number): ")
        while not state.validate_move(move):
            move = input("Please enter a valid move: ")
        return Connect4Move(int(move))


if __name__ == '__main__':
    # Setup
    GAME_TYPE = "connect_4"
    username = input("Enter username: ")
    # Create game ?
    game_id = input("Enter your game_id, or anything else to create a game: ")
    if game_id[0:5] != "game_":
        game_id = wrapper.GenericGameClient.create_game("connect_4")
    print("Using game_id: {}".format(game_id))
    # Join game ?
    client = wrapper.GenericGameClient(GAME_TYPE, game_id, username)
    client.join_game()
    # Now wait until others join
    state = Connect4State()
    client.update_state(state)
    while state.is_waiting_for_start():
        while not client.wait_for_update():
            continue
        client.update_state(state)
        print("Waiting")
    # Now players should have joined and the game started
    print("Game started.")
    # Initialise connect-4 agent
    agent = Connect4Agent()
    while state.is_in_progress():
        # If you can make move
        if state.player_can_move(client.username):
            # Make Move
            client.submit_move(move=agent.make_move(state, client))
        # Spin while waiting for update
        while not client.wait_for_update():
            continue
        client.update_state(state)

    # Game Ended
    if client.username in state.winners:
        print("You won")
    else:
        print("You lost")
