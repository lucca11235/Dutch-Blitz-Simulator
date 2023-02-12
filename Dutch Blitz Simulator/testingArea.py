from player import Player
from game import Game
from tqdm import tqdm
import time

g = Game()

p1 = Player(g, '1', 1.2)
p2 = Player(g, '2', 2.2)
p3 = Player(g, '3', 1.5)
p4 = Player(g, '4', 1.7)

g.initialize_players()
g.print_players()

start = time.time()
g.simulate(print_simulation=True,print_results=True, return_stat=True)

