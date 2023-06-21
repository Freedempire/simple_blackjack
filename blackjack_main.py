import time

from blackjack_info import BLACKJACK_ASCII, RULES
from blackjack import Blackjack

print(BLACKJACK_ASCII)
print(RULES)

game = Blackjack()
game.initialize_game()

while game.player.money > 0:
    game.place_wager_or_quit()
    game.deal_initial()
    game.show_participant_info(game.dealer)
    game.show_participant_info(game.player)
    game.process_initial()
    time.sleep(0.5)
    game.player_turn()
    time.sleep(0.5)
    game.dealer_turn()
    time.sleep(0.8)
    game.get_result()
    time.sleep(0.8)
    game.round_state_reset()

print('You have lost all of your money. Game finished.')