from card import Card

class Stack:
    def __init__(self, top_card: Card):
        self.pile = [top_card]
        self.top_card = top_card

    def add_card(self, card):
        self.pile.append(card)
        self.top_card = card

    def __repr__(self):
        return f'{self.top_card}'