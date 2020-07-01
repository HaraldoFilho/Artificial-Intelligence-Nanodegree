"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)

        self.minimax_player1 = game_agent.MinimaxPlayer()
        self.minimax_player2 = game_agent.MinimaxPlayer()
        self.minimax_game = isolation.Board(self.minimax_player1, self.minimax_player2)

        self.alphabeta_player1 = game_agent.AlphaBetaPlayer()
        self.alphabeta_player2 = game_agent.AlphaBetaPlayer()
        self.alphabeta_game = isolation.Board(self.alphabeta_player1, self.alphabeta_player2)

    def test_time_left(self):
        return 10

    def test_minimax(self):
        self.minimax_player1.time_left = self.test_time_left
        print("")
        for i in range(1, 5):
            p1_best_move = self.minimax_player1.minimax(self.minimax_game, i)
            print("Player 1 minimax best move on {0} levels deep = {1}".format(i, p1_best_move))

    def test_alphabeta(self):
        self.alphabeta_player1.time_left = self.test_time_left
        print("")
        for i in range(1, 5):
            p1_best_move = self.alphabeta_player1.alphabeta(self.alphabeta_game, i)
            print("Player 1 alphabeta best move = {0}".format(p1_best_move))

if __name__ == '__main__':
    unittest.main()
