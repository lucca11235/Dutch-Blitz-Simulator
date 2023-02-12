from stacks import Stack
from typing import List
from player import Player
import numpy as np
import random
from card import Card
from scipy.stats import norm
import time


class Game:
    def __init__(self):
        self.stacks: List[Stack] = []
        self.players: List[Player] = []
        self.timer = 0

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def add_stack(self, card: Card) -> None:
        self.stacks.append(Stack(card))

    def print_players(self) -> None:
        for player in self.players:
            player.print_player()

    def initialize_players(self) -> None:
        for player in self.players:
            player.initialize()

    def create_random_players(self,
                              number_players: int,
                              mean: float,
                              std: float) -> None:
        """
        :param number_players: The number of players that will be created
        :param mean: The mean of the action times
        :param std: The standard deviation of action times
        :return: Creates N players with random action times according to mean and std
        """
        for i in range(1, number_players + 1):
            z_score = norm.ppf(random.random())
            x = z_score * std + mean
            Player(self, f'{i}', x)

    def turn(self,
             print_turn: bool = False) -> None:
        if print_turn: print('\n')
        """
        This method plays one turn of the game. The algorithm is as follows:
        1. Look at each players curr_t
        2. Get the player with the least curr_t
        3. Update each player's curr_t and the game's timer 
        4. Let the player with least curr_t play
        """
        values = [player.curr_t for player in self.players]  # 1.

        # 2. if two players have the same min val, then the player will be randomly selected
        min_val = min(values)
        indexes = [i for i, n in enumerate(values) if n == min_val]
        index_min = random.choice(indexes)

        # 3.
        self.timer += min_val
        for player in self.players:
            player.curr_t -= min_val

        # 4.
        if print_turn:
            self.print_players()
            print(f'Stacks: {self.stacks}')

        self.players[index_min].play(print_play=print_turn)

        if print_turn: print('\n')

    def check_blitz(self) -> bool:
        for player in self.players:
            if len(player.main) == 0:
                return player
        return 0

    def num_cards_on_deck(self) -> int:
        num_cards = 0
        for stack in self.stacks:
            num_cards += len(stack.pile)
        return num_cards

    def players_final_score(self,
                            print_final_score=False) -> List[int]:
        final_scores = []
        for player in self.players:
            final_scores.append(player.player_score())

        if print_final_score:
            print('--Final scores--')
            for player in self.players:
                print(f'\tPlayer {player.name}: {player.player_score()}')
        return final_scores

    def simulate(self,
                 print_simulation=False,
                 print_results=False,
                 return_stat=False) -> Player:

        num_turns: int = 0
        average_of_cards_players = [player.average_cards_num() for player in self.players]
        players_act_times = [player.act_t for player in self.players]

        start_time = time.time()
        while not (winner := self.check_blitz()):
            if time.time() - start_time > 0.1:
                return
            self.turn(print_turn=print_simulation)
            num_turns += 1

        made_blitz = [[0, 1][player == winner] for player in self.players]
        if print_results:
            execution_time = time.time() - start_time
            print(f'Player {winner.name} BLITZ!!!\n')
            self.players_final_score(print_final_score=True)
            print(f'\n--Game Stats-- \n'
                  f'\tNumber of turns: {num_turns}\n'
                  f'\tNumber of cards: {self.num_cards_on_deck()}\n'
                  f'\tTotal time of game: {round(self.timer, 2)}\n'
                  f'\tAverage Final Scores: {np.mean(self.players_final_score())}\n'
                  f'\tStd Final Scores: {np.std(self.players_final_score())}\n'
                  f'\tExecution time: {execution_time}s')
        if return_stat:
            return average_of_cards_players, players_act_times, self.players_final_score(), made_blitz
        return winner
