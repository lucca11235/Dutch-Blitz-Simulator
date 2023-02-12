class Card:
    def __init__(self, num, color):
        self.num = num
        self.color = color

    def __repr__(self):
        return f'({self.num},{self.color})'
