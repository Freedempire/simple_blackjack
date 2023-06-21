"""Contains blackjack ascii art and rules information."""

BLACKJACK_ASCII = """
 _     _            _    _            _    
| |   | |          | |  (_)          | |      ___   ___
| |__ | | __ _  ___| | ___  __ _  ___| | __  |A  | |K  |
| '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /  | ♠ | | ♦ |
| |_) | | (_| | (__|   <| | (_| | (__|   <   |__A| |__K|
|_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
                       _/ |                
                      |__/   
"""

RULES = """
Rules:
  Try to get as close to 21 without going over.
  Kings, Queens, and Jacks are worth 10 points.
  Aces are worth 1 or 11 points.
  Cards 2 through 10 are worth their face value.
  (H)it to take another card.
  (S)tand to stop taking cards.
  On your first play, you can (D)ouble down to increase your
    bet but must hit exactly one more time before standing.
  You can also su(R)render on your inital bet to get half of
    your wager back, if the dealer's hand is not a blackjack.
  In the case of a tie, the bet is returned to the player.
  The dealer stops hitting at 17.
"""