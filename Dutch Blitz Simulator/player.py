from handsCard import Cards
from stacks import Stack
from typing import List


def print_statement(bool_val, stat):
    if bool_val:
        print(stat)


class Player(Cards):
    def __init__(self, game, name: str, act_t: float):
        super().__init__()
        self.game = game
        self.name: str = name
        self.act_t: float = act_t
        self.curr_t: float = act_t

        self.points: int = 0

        self.game.add_player(self)

    def print_player(self):
        print(f'Player: {self.name} '
              f'Points:{self.points} '
              f'Curr_t: {round(self.curr_t, 2)} '
              f'Cards: {self.buffers} {self.main[-1]}{len(self.main)}  {self.hand[self.hand_index]}{len(self.hand)} {self.hand_index}')

    def average_cards_num(self):
        final_sum = 0
        for buffer in self.buffers: final_sum += buffer.num
        final_sum += self.main[-1].num
        return final_sum / 4

    def player_score(self):
        return self.points - 2 * len(self.main)

    def check_card(self, card):
        """
         This functions checks each stack on the deck and look
         whether the card is throwable, if it is, then it
         automatically throws it
        """
        if card.num == 1:
            self.game.add_stack(card)
            return 1
        for stack in self.game.stacks:
            top = stack.top_card
            if (top.num == card.num - 1) and (top.color == card.color):
                stack.add_card(card)
                return 1

        return 0

    def play(self, print_play=False):
        if not self.main:
            return 1

        self.curr_t = self.act_t

        # Check for main card
        main_card = self.main[-1]
        if self.check_card(main_card):
            self.main.pop()
            self.points += 1
            print_statement(print_play, f'Player {self.name} Pop Main {main_card}!')
            return

        # Check for the buffers
        for i in range(3):
            buffer = self.buffers[i]
            if self.check_card(buffer):
                self.buffers[i] = self.main.pop()  # Place a main stack card on it's place
                self.points += 1
                print_statement(print_play, f'Player {self.name} Pop Buffer {buffer}!')
                return

        # Check hand card
        hand_card = self.hand[self.hand_index]
        if self.check_card(hand_card):
            self.hand.pop(self.hand_index)
            self.flip_hand()
            self.points += 1
            print_statement(print_play, f'Player {self.name} Pop Hand {hand_card}')
            return

        self.flip_hand()
        new_hand = self.hand[self.hand_index]
        print_statement(print_play, f'Player {self.name} Flipped Hand {hand_card} -> {new_hand}')
