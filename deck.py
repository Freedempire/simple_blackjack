import random

import card

class Deck:
    """Class representing the deck of blackjack game. The deck of the game can
    have multiple 52-card decks."""
    def __init__(self, number_of_decks=1):
        # The number of 52-card decks in the game deck.
        self.number_of_decks = number_of_decks
        self.cards = self.get_cards()

    def get_cards(self):
        """Generates cards for the deck of the game."""
        single_deck = []
        cards = []
        for suit in card.SUITS.values():
            for rank in card.RANKS:
                single_deck.append(card.Card(suit, rank))
        for _ in range(self.number_of_decks):
            cards += single_deck[:]
        return cards
    
    def shuffle_cards(self):
        random.shuffle(self.cards)

if __name__ == '__main__':
    deck = Deck(2)
    deck.shuffle_cards()
    for card in deck.cards:
        print(card)
    print(len(deck.cards))
    print(deck.cards.pop())