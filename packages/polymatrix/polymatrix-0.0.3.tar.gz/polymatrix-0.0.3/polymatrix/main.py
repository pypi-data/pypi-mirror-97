import os, random
import numpy as np
from .logger import log
from .player import Player
from .polymatrixgame import PolymatrixGame
from pprint import pprint
import itertools
from collections import defaultdict


class GameManager:
    def __init__(self, number_of_players=3):
        self.number_of_players = number_of_players
        pass

    def get_random_players(self, lower_bound=0, upper_bound=100):
        n = self.number_of_players
        players = [
            [random.randint(lower_bound, upper_bound), random.randint(lower_bound, upper_bound)] for i in range(n)
        ]
        return players

    def get_random_strategy_profile(self):
        n = self.number_of_players
        strategy_profile = [random.randint(0, 1) for i in range(n)]
        return strategy_profile

class QuickPolymatrixGame(PolymatrixGame):
    def __init__(self, number_of_players=3, timesteps=0, log_level="warning"):
        manager = GameManager(number_of_players)
        players = manager.get_random_players()

        game_settings = {
            "start_populations_matrix": players,
            "topology": "fully_connected",
            'alpha': 1.0,
            'log_level': log_level
        }
        self = super().__init__(**game_settings)
        self.manager = manager
        self.game_settings = game_settings
        self.timesteps = timesteps
        self.simulate()

    def simulate(self):
        print(f"Simulated for {len(self.players)} players")
        print(f" Network topology: {self.game_settings['topology']}")
        print(f" Game state {self.state.tolist()}")
        for i in range(self.timesteps):
            self.play(self.manager.get_random_strategy_profile())
            print(f" Strategy profile: {self.strategy_profile}")
            print(f" Game state {self.state.tolist()}")

class QuickGame(PolymatrixGame):
    def __init__(self, number_of_players=3, topology="random", log_level="warning"):
        manager = GameManager(number_of_players)
        players = manager.get_random_players()

        game_settings = {
            "start_populations_matrix": players,
            "topology": topology,
            'alpha': 1.0,
            'log_level': log_level
        }
        self = super().__init__(**game_settings)

    def simulate(self, timesteps = 3):
        self.manager = GameManager(len(self.players))
        self.timesteps = timesteps
        print(f"Simulated for {len(self.players)} players")
        print(f" Network topology: {self.network.edges}")
        print(f" Game state {self.state.tolist()}")
        for i in range(self.timesteps):
            self.play(self.manager.get_random_strategy_profile())
            print(f" Strategy profile: {self.strategy_profile}")
            print(f" Game state {self.state.tolist()}")