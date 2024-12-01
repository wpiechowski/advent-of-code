import time

from tools import *
import numpy as np


config_i = {
    "players": 441,
    "last": 7103200,
}

config_s = {
    "players": 10,
    "last": 1618,
}


def play(n_marbles: int, n_players: int):
    scores = np.zeros((n_players,), int)
    board = np.zeros((n_marbles,), int)
    count = 1
    player = 0
    pos = 0
    t = time.time()
    for marble in range(1, n_marbles):
        now = time.time()
        if now - t > 1:
            t = now
            ic(marble / n_marbles)
        if marble % 23 == 0:
            scores[player] += marble
            del_pos = (pos - 7) % count
            scores[player] += board[del_pos]
            if del_pos == count - 1:
                count -= 1
                pos = 0
            else:
                pos = del_pos
                board[pos: count - 1] = board[pos + 1: count]
                count -= 1
        else:
            insert_pos = (pos + 2) % count
            if insert_pos == 0:
                board[count] = marble
                pos = count
                count += 1
            else:
                board[insert_pos + 1: count + 1] = board[insert_pos: count]
                board[insert_pos] = marble
                count += 1
                pos = insert_pos
        player = (player + 1) % n_players
        # ic(pos, board[:count])
    return scores


def task1():
    config = config_i
    n_players = config["players"]
    n_marbles = config["last"] + 1
    scores = play(n_marbles, n_players)
    ic(max(scores))
