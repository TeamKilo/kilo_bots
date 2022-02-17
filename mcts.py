# TODO: test if it works :)

import math
import sys
import time
from typing import List, Tuple, Optional

from utils import Connect4State
from copy import deepcopy

import random

BOARD_WIDTH = Connect4State.GAME_BOARD_WIDTH
BOARD_HEIGHT = Connect4State.GAME_BOARD_HEIGHT

DEBUG = True


class Node:
    def __init__(self, parent: Optional['Node'],
                 state: List[List[str]], children: List['Node'],
                 last_player: str, last_move: Optional[int] = None):
        self.parent = parent
        self.state = state
        # Children states that have been selected once at least
        self.children = children
        # will be 'O' or 'X': WHO HAD JUST PLAYED to get to this state. Corresponds to the colour of the node.
        self.last_player = last_player
        self.last_move = last_move
        # (Wins for [colour], Play-outs from this node)
        self.visits = 0
        self.wins = 0


# Assume that the game state is represented as a list of lists, each one corresponding to a column.


def step(state: List[List[str]], turn: str, move: int, copy=False):
    """ returns True if move made; else false
    :param copy: perform deep copy if set to true, otherwise just step it
    :param turn 1 or -1
    :param state
    :param move
    """
    if len(state[move]) >= BOARD_HEIGHT:
        return None

    if copy:
        n_state = deepcopy(state)
        n_state[move].append(turn)
        return n_state
    else:
        state[move].append(turn)
        return state


def valid_moves(state: List[List[str]]) -> Tuple[List[int], Optional[str]]:
    # if game ended, then just return empty list
    winner = check_win(state)
    if winner is not None: return ([], winner)
    # else game is continuing
    valid_move_list = []
    for move in range(len(state)):
        if len(state[move]) < BOARD_HEIGHT:
            valid_move_list.append(move)
    return (valid_move_list, None)


def check_win(state: List[List[str]]):
    """ Returns 'O' or 'X' if winner, 'draw' if draw and None if not ended yet """
    # Draw
    if all([len(col) == BOARD_HEIGHT for col in state]):
        return 'draw'
    # Who wins
    # cols
    if DEBUG: print("Scanning columns")
    current_p = 'O'
    current_count = 0
    for column in state:
        for el in column:
            if el == current_p:
                current_count += 1
                if current_count == 4:
                    return current_p
            else:
                current_count = 1
                current_p = el
        current_count = 0
        current_p = 'O'

    # Rows
    if DEBUG: print("Scanning rows")
    for row_num in range(BOARD_HEIGHT):
        row = [col[row_num] if len(col) > row_num else None for col in state]
        for el in row:
            if el is None:
                current_count = 0
                continue
            if el == current_p:
                current_count += 1
                if current_count == 4:
                    return current_p
            else:
                current_count = 1
                current_p = el
        current_count = 0
        current_p = 'O'

    # Diagonal - top left to bottom right, x is first arg of list, y is second
    if DEBUG: print("Scanning diagonals with horizontal offset")
    max_x_offset = BOARD_WIDTH - 4  # value=3
    for x_init_offset in range(max_x_offset + 1):
        diagonal1 = [state[x_init_offset + i][i]
                     if x_init_offset + i < BOARD_WIDTH and i < len(state[x_init_offset + i])
                     else None
                     for i in range(min(BOARD_WIDTH - x_init_offset, BOARD_HEIGHT))]
        diagonal2 = [state[(BOARD_WIDTH - x_init_offset - 1) - i][i]
                     if (BOARD_WIDTH - x_init_offset - 1) - i >= 0
                        and i < len(state[(BOARD_WIDTH - x_init_offset - 1) - i]) else None
                     for i in range(min(BOARD_WIDTH - x_init_offset, BOARD_HEIGHT))]
        for diagonal in [diagonal1, diagonal2]:
            for el in diagonal:
                if el is None:
                    current_count = 0
                    continue
                if el == current_p:
                    current_count += 1
                    if current_count == 4:
                        return current_p
                else:
                    current_count = 1
                    current_p = el
            current_count = 0
            current_p = 'O'
    if DEBUG: print("Scanning diagonals with vertical offset")
    max_y_offset = BOARD_HEIGHT - 4
    for y_init_offset in range(max_y_offset + 1):
        diagonal1 = [state[i][y_init_offset + i] if y_init_offset + i < len(state[i]) else None for i in
                     range((min(BOARD_HEIGHT - y_init_offset, BOARD_WIDTH)))]
        diagonal2 = [state[i][(BOARD_HEIGHT - y_init_offset - 1) - i]
                     if 0 <= (BOARD_HEIGHT - y_init_offset - 1) - i < len(state[i]) else None for i in
                     range(min(BOARD_HEIGHT - y_init_offset, BOARD_WIDTH))]
        for diagonal in [diagonal1, diagonal2]:
            for el in diagonal:
                if el is None:
                    current_count = 0
                    continue
                if el == current_p:
                    current_count += 1
                    if current_count == 4:
                        return current_p
                else:
                    current_count = 1
                    current_p = el
            current_count = 0
            current_p = 'O'
    return None


def uct_value(parent_visit, node_visit, node_wins):
    if node_visit == 0:
        return sys.maxsize
    return node_wins / node_visit + math.sqrt(2 * math.log(parent_visit) / node_visit)


def uct_children(node: Node):
    parent_visit = node.visits
    children_uct_values = list(map(lambda n: uct_value(parent_visit, n.visits, n.wins), node.children))
    return children_uct_values


# Probabilistic approach
def uct_children_sample(node: Node) -> Node:
    children_uct_values = uct_children(node)
    return random.choices(node.children, children_uct_values)[0]


def get_opponent(player):
    if player == 'O':
        return 'X'
    else:
        return 'O'


def select(node: Node):
    tmp = node
    while len(tmp.children) > 0:
        tmp = uct_children_sample(tmp)
    # Now reach leaf node
    return tmp


def expand(node: Node):
    """
    Expand phase of MCTS: find a leaf node and expand it

    :param node: a leaf node of the search tree to be expanded
    :returns: None if it's a terminal node, or Some(Node) a random child constructed after the expansion
    """
    assert len(node.children) == 0
    (valid_move_list, _) = valid_moves(node.state)
    if len(valid_move_list) == 0:
        return None
    node.children += [Node(parent=node,
                           state=step(state=node.state, turn=get_opponent(node.last_player), move=move, copy=True),
                           children=[],
                           last_player=get_opponent(node.last_player),
                           last_move=move)
                      for move in valid_move_list]
    # Note: valid_moves returns the empty list if the game has ended.
    return random.choice(node.children)


def rollout_policy(possible_moves):
    return random.choice(possible_moves)


def rollout(node: Node):
    """
    Rollout phase.

    :param node: the leaf node you want to rollout
    :return: the player who won
    """
    state = node.state
    next_player = get_opponent(node.last_player)
    (possible_moves, winner) = valid_moves(state)
    while len(possible_moves) > 0:
        state = step(state, next_player, rollout_policy(possible_moves), copy=False)
        next_player = get_opponent(next_player)
    return winner


def backpropagate(node: Node, winner: str):
    tmp_node = node
    while tmp_node is not None:
        tmp_node.visits += 1
        if tmp_node.last_player == winner:
            tmp_node.wins += 1
        elif winner == 'draw':
            tmp_node.wins += 0.5
        tmp_node = tmp_node.parent


def best_child(node: Node):
    return max(node.children, key=lambda n: n.visits)


def mcts(state: List[List[str]], turn: str, time_limit: float):
    """
    :param state: state of board
    :param turn: 'O' or 'X': indicates who's turn it is
    :param time_limit: in seconds, please be conservative because this isn't a strict limit
    :return: integer from 0 to BOARD_WIDTH-1 to indicate the move
    """
    opponent = get_opponent(turn)
    root = Node(None, state, children=[], last_player=opponent, last_move=None)
    max_time = time.time() + time_limit
    while time.time() < max_time:
        promising_node = select(root)
        leaf = expand(promising_node)
        if leaf is None:
            leaf = promising_node
        simulation_result = rollout(leaf)
        backpropagate(leaf, simulation_result)
    return best_child(root).last_move


if __name__ == '__main__':
    print(check_win([['X', 'X', 'O', 'X', 'X', 'O'],
                     ['X', 'X', 'X'],
                     ['O', 'O', 'O', 'X'],
                     ['X', 'O', 'O', 'X', 'X'],
                     ['X', 'X', 'X', 'O', 'O'],
                     ['X', 'X', 'X', 'O', 'X', 'X'],
                     []]))

# Note: inspired from
# https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
# https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
# https://www.baeldung.com/java-monte-carlo-tree-search
