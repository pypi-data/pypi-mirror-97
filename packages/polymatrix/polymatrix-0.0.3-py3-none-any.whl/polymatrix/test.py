import unittest
from .polymatrixgame import PolymatrixGame
from .player import Player

game = PolymatrixGame()

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(population_vector=[1,2], index=1)

    def test_player_history(self):
        self.assertTrue(self.player.history==[])

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = PolymatrixGame()

    def test_object_instantiation(self):
        self.assertTrue(
            self.game != None, "Game was not instantiated so self.game==None"
        )

    def test_class_type(self):
        self.assertTrue(
            str(self.game.__class__) == "<class 'polymatrix.polymatrixgame.PolymatrixGame'>",
            f"Type of object is not <class 'polymatrix.polymatrixgame.PolymatrixGame'> but rather {self.game.__class__}",
        )

    def test_game_empty(self):
        self.assertTrue(
            self.game.players == None, "In empty game there are no players."
        )

    def test_def_initiate_players(self):
        self.assertTrue(
            self.game.initiate_players(start_populations_matrix=[[3, 0], [1, 2], [2, 1]]),
            "Player initiation failed",
        )

    def test_def_get_state(self):
        self.game.initiate_players(start_populations_matrix=[[3, 0], [1, 2], [2, 1]])
        self.assertTrue(
            self.game.get_state(),
            "Getting state failed",
        )

    def test_def_set_strategy_profile(self):
        self.game.initiate_players(start_populations_matrix=[[3, 0], [1, 2], [2, 1]])
        self.assertTrue(
            self.game.set_strategy_profile([0, 1, 1]),
            "Setting strategy profile failed",
        )

    def test_functionality_set_strategy_profile(self):
        self.game.initiate_players(start_populations_matrix=[[3, 0], [1, 2], [2, 1]])
        self.game.set_strategy_profile([0, 1, 1])
        with self.assertRaises(AttributeError):
            self.game.play() # should throw an error because there are no edges in the graph yet

    def test_functionality_play(self):
        with self.assertRaises(TypeError):
            self.game.play() # should throw an error because there are no players in the graph yet


if __name__ == "__main__":
    unittest.main()
