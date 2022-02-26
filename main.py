import sys

import clientlib.wrapper as wrapper
from connect_4.agents import Connect4InteractiveAgent, Connect4RandomAgent, Connect4MCTSAgent
from connect_4.utils import Connect4State
import argparse

from connect_4.your_own_bot import Connect4UserDefinedAgent
from snake.agents import SnakeInteractiveAgent, SnakeRandomAgent
from snake.your_own_bot import SnakeUserDefinedAgent


def main(agent, username, game_id, game_type):
    # Create game ?
    if game_id is None or game_id[0:5] != "game_":
        game_id = wrapper.GenericGameClient.create_game("connect_4")
    print("Using game_id: {}".format(game_id))
    # Join game ?
    client = wrapper.GenericGameClient(game_type, game_id, username)
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
        # If you can make move
        if state.player_can_move(client.username):
            print(state)
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
    parser = argparse.ArgumentParser(description="Main script for the game client.")
    parser.add_argument('-t', '--type', type=str, help="type of game, currently supported "
                                                       "are connect_4 and snake",
                        required=True)
    parser.add_argument('-a', '--agent', type=str, help="the agent to be run: i for interactive; r "
                                                        "for random; u for user-defined; "
                                                        "(only if game type is connect_4) "
                                                        "[m1|m3|m5 for MCTS agent with deterministic "
                                                        "selection and 1|3|5 seconds time; m10p for one with "
                                                        "probabilistic selection and 5|10 seconds time.]",
                        required=True)
    parser.add_argument('-u', '--username', type=str, help="the username given to the bot.", required=True)
    parser.add_argument('-g', '--game', type=str, help='the game id. If None, will create a new game.')
    parsed_args = parser.parse_args(sys.argv[1:])

    connect_4_agent_map = {
        "i": Connect4InteractiveAgent(),
        "r": Connect4RandomAgent(),
        "m1": Connect4MCTSAgent(parsed_args.username, 1, False),
        "m3": Connect4MCTSAgent(parsed_args.username, 3, False),
        "m5": Connect4MCTSAgent(parsed_args.username, 5, False),
        "m10p": Connect4MCTSAgent(parsed_args.username, 10, True),
        "c": Connect4UserDefinedAgent()
    }

    snake_agent_map = {
        "i": SnakeInteractiveAgent(),
        "r": SnakeRandomAgent(parsed_args.username),
        "c": SnakeUserDefinedAgent(parsed_args.username)
    }

    if parsed_args.type == "connect_4":
        if parsed_args.agent not in connect_4_agent_map:
            print("Agent not found")
        else:
            main(connect_4_agent_map[parsed_args.agent], parsed_args.username, parsed_args.game, parsed_args.type)
    elif parsed_args.type == "snake":
        if parsed_args.agent not in snake_agent_map:
            print("Agent not found")
        else:
            main(snake_agent_map[parsed_args.agent], parsed_args.username, parsed_args.game, parsed_args.type)
    else:
        print("Game type invalid")
