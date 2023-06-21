# Unicode has code points for the 52 cards of the standard French deck plus the
# Knight (Ace, 2-10, Jack, Knight, Queen, and King for each suit), two for black
# and white (or red) jokers and a back of a card, in block Playing Cards
# (U+1F0A0–1F0FF).
# https://en.wikipedia.org/wiki/Playing_cards_in_Unicode

SUITS = {'CLUBS': '♣', 'DIAMONDS': '♦', 'HEARTS': '♥', 'SPADES': '♠'}
RANKS = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
         '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': (1, 11)}

class Card:
    """Class for single card."""

    # it seems the @staticmethod is unnecessary here
    # both work with or without the decorator
    @staticmethod
    def generate_backside():
        row_0 = (' ___ ')
        row_1 = f'|## |'
        row_2 = f'| # |'
        row_3 = f'|_##|'
        return [row_0, row_1, row_2, row_3]

    # Every single card share the same backside.
    backside = generate_backside()

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = RANKS[self.rank]
        self.frontside = self.generate_frontside()
    
    def generate_frontside(self):
        row_0 = (' ___ ')
        row_1 = f'|{self.rank:<2} |'
        row_2 = f'| {self.suit} |'
        row_3 = f'|_{self.rank:_>2}|'
        return [row_0, row_1, row_2, row_3]
    
    def __str__(self):
        return str((self.suit, self.rank))

if __name__ == '__main__':
    print(Card(SUITS['CLUBS'], '10').frontside)
    print(Card.backside)