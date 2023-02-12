import random
from card import Card


class Cards:
    def __init__(self):
        self.buffers = None
        self.main = None
        self.hand = None
        self.hand_index = 0

    def initialize(self):
        r = [Card(i, 'r') for i in range(1, 11)]
        b = [Card(i, 'b') for i in range(1, 11)]
        g = [Card(i, 'g') for i in range(1, 11)]
        y = [Card(i, 'y') for i in range(1, 11)]

        cards = r + b + g + y
        random.shuffle(cards)

        self.main = cards[:10]
        del cards[:10]

        self.buffers = cards[:3]
        del cards[:3]

        self.hand = cards
        del cards

    def flip_hand(self):
        L = len(self.hand)
        index = self.hand_index
        if index + 3 >= L:
            self.hand_index = random.choice([0, 1, 2])
        else:
            self.hand_index = index + 3

    def __repr__(self):
        return f'{self.buffers}   {self.main[-1]}{len(self.main)}    {self.hand[self.hand_index]}'
