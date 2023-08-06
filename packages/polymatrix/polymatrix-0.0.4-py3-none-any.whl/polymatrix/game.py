import plac
from polymatrixgame import QuickPolymatrixGame

@plac.annotations(number_of_players=("Amount of players", "option", "n", int),
                    log_level=("Preferred level of logging", "option", "log", str),
                    timesteps=("Amount of rounds to be played", "option", "t", int))
def main(number_of_players=3, timesteps=0, log_level="warning"):
    QuickPolymatrixGame(number_of_players, timesteps, log_level)

if __name__ == "__main__":
    plac.call(main)
    
