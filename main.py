import sys

import clientlib.wrapper as wrapper
from agents import Connect4InteractiveAgent, Connect4RandomAgent, Connect4BaseAgent
from utils import Connect4State, Connect4Move
import argparse

GAME_TYPE = "connect_4"


def main(agent: Connect4BaseAgent, username=None, game_id=None):
    # Setup
    if username is None:
        username = input("Enter username: ")
    # Create game ?
    if game_id is None:
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
    while state.is_in_progress():
        print(state)
        # If you can make move
        if state.player_can_move(client.username):
            # Make Move
            client.submit_move(move=agent.get_next_move(state))
            client.update_state(state)
            print(state)
            if state.is_ended(): break
        # Spin while waiting for update
        while not client.wait_for_update():
            print("Waiting")
            continue
        client.update_state(state)

    # Game Ended
    if client.username in state.winners:
        print("You won")
    else:
        print("You lost")
    print(state)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Main script for the game client")
    parser.add_argument('-a', '--agent', type=str, help="the agent to be run: i for interactive; r "
                                                        "for random", required=True)
    parser.add_argument('-u', '--username', type=str, help="the username given to the bot")
    parser.add_argument('-g', '--game', type=str, help='the game id')
    agent_map = {
        "i": Connect4InteractiveAgent(),
        "r": Connect4RandomAgent()
    }
    parsed_args = parser.parse_args(sys.argv[1:])
    main(agent_map[parsed_args.agent], parsed_args.username, parsed_args.game)
