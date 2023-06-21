import sys

from deck import Deck
from participant import Player, Dealer

class Blackjack:
    def __init__(self):
        self.deck_limit = 4
        self.money_limit = 10000
        self.bet_limit = 5000
        self.possible_actions = {
            'hit': '(H)it',
            'stand': '(S)tand',
            'double down': '(D)ouble down',
            'surrender': 'su(R)render'
        }
        self.deck_penetration = 0.7

    def initialize_game(self):
        self.get_number_of_decks()
        self.prepare_deck()
        self.get_dealer()
        self.get_player()
        self.round_state_reset()

    def round_state_reset(self):
        self.check_penetration()
        self.dealer.new_round()
        self.player.new_round()
        self.player_initial_deal = True
        self.player_stood = False
        self.player_lost = False
        self.player_surrendered = False
        self.player_blackjacked = False
        
    def check_penetration(self):
        # print(f'cards left: {len(self.deck)}')
        # print(f'deck penetration: {1 - len(self.deck) / self.number_of_decks / 52}')
        if len(self.deck) / self.number_of_decks / 52 < 1 - self.deck_penetration:
            print('Card penetration reached, preparing new deck . . .')
            self.prepare_deck()

    def get_integer_input(self, message, limit, name, exception=None):
        while True:
            try:
                input_text = input(message).lower()
                if exception and input_text == exception.lower():
                    return input_text
                integer = int(input_text)
                if integer < limit[0] or integer > limit[1]:
                    raise ValueError
                return integer
            except ValueError:
                print(f'The {name} should be an integer between {limit[0]} and {limit[1]}.')

    def get_nonempty_string(self, message, name):
        while True:
            nonempty_string = input(message)
            if len(nonempty_string) == 0:
                print(f'The {name} should not be empty.')
                continue
            return nonempty_string

    def get_number_of_decks(self):
        message = f'Number of 52-card decks for this game (1-{self.deck_limit})\n > '
        self.number_of_decks = self.get_integer_input(message, (0, self.deck_limit), 'number of decks')
        print()

    def prepare_deck(self):
        deck = Deck(self.number_of_decks)
        deck.shuffle_cards()
        self.deck = deck.cards

    def get_dealer(self):
        self.dealer = Dealer()

    def get_player(self):
        message = f'How much do you have for the game? (1-{self.money_limit})\n > '
        money = self.get_integer_input(message, (0, self.money_limit), 'money')
        self.player = Player(money)
        print()

    def place_wager_or_quit(self):
        print(f'Money: {self.player.money}')
        message = f'How much do you bet? (1-{min(self.bet_limit, self.player.money)}, q for quit)\n> '
        bet = self.get_integer_input(message, (1, min(self.bet_limit, self.player.money)), 'bet', 'q')
        if bet == 'q':
            print('Bye.')
            sys.exit()
        self.player.bet(bet)
        print()
        
    def get_points(self, participant):
        participant.calculate_points()

    def deal_single(self, participant):
        participant.hand.append(self.deck.pop())
        self.get_points(participant)

    def deal_initial(self):
        for _ in range(2):
            self.deal_single(self.player)
            self.deal_single(self.dealer)

    def show_cards(self, participant):
        for row_index in range(len(participant.hand[0].frontside)):
            for card_index in range(len(participant.hand)):
                if self.player_initial_deal and participant.role == 'dealer' and card_index == 0:
                    print(participant.hand[card_index].backside[row_index], end=' ')
                else:
                    print(participant.hand[card_index].frontside[row_index], end=' ')
            print()
        print()

    def show_points(self, participant):
        if participant.role == 'dealer':
            if self.player_initial_deal:
                print('Dealer: ???')
            else:
                print(f'Dealer: {participant.points}')
        else:
            print(f'Player: {participant.points}')

    def show_participant_info(self, participant):
        self.show_points(participant)
        self.show_cards(participant)

    def process_initial(self):
        if self.dealer.points == 21: 
            if self.player.points < 21:
                self.player_lost = True
            self.player_initial_deal = False
        if self.player.points == 21:
            self.player_blackjacked = True
            self.player_initial_deal = False

    def player_turn(self):
        while not (self.player_stood or self.player_lost or self.player_surrendered or self.player_blackjacked):
            actions_list = list(self.possible_actions.values())
            if not self.player_initial_deal:
                actions_list.remove(self.possible_actions['surrender'])
                actions_list.remove(self.possible_actions['double down'])
            elif self.player.money < self.player.wager:
                actions_list.remove(self.possible_actions['double down'])
                
            actions_direction = [direction[direction.find('(') + 1].lower() for direction in actions_list]

            message = f'{", ".join(actions_list)}\n> '
            while True:
                player_direction = self.get_nonempty_string(message, 'direction')
                print()
                if player_direction.lower() not in actions_direction:
                    print(f'The direction should be one of {", ".join(actions_direction)}.\n')
                    continue
                break
            match player_direction:
                case 'h':
                    self.hit()
                    self.show_participant_info(self.player)
                    self.process_player()
                case 's':
                    self.stand()
                case 'd':
                    if self.double_down():
                        self.show_participant_info(self.player)
                        self.process_player()
                case 'r':
                    self.surrender()
            self.player_initial_deal = False
        
    def hit(self):
        self.deal_single(self.player)

    def stand(self):
        self.player_stood = True

    def double_down(self):
        if self.player.double_down():
            self.hit()
            return True
        print('You don\'t have enough money to double down.')
        return False
        
    def surrender(self):
        self.player_surrendered = True

    def process_player(self):
        if self.player.points == 21:
            self.player_stood = True
        elif self.player.points > 21:
            self.player_lost = True
        
    def dealer_turn(self):
        while not (self.player_lost or self.player_blackjacked or self.player_surrendered) and self.dealer.points < 17:
            self.deal_single(self.dealer)
        self.show_participant_info(self.dealer)
        
    def get_result(self):
        result = ''
        if self.player_blackjacked:
            if self.dealer.points == 21:
                result = 'push'
            else:
                result = 'player won'
        elif self.player_surrendered:
            result = 'player surrendered'
        elif self.player_lost:
            result = 'player lost'
        elif self.dealer.points < self.player.points or self.dealer.points > 21:
            result = 'player won'
        elif self.dealer.points == self.player.points:
            result = 'push'
        else:
        # elif self.player.points < self.dealer.points <= 21:
            result = 'player lost'

        match result:
            case 'push':
                self.player.money += self.player.wager
                print('Push.')
            case 'player won':
                self.player.money += self.player.wager * 2
                print(f'Player won ${self.player.wager}.')
            case 'player lost':
                print(f'Player lost ${self.player.wager}.')
            case 'player surrendered':
                self.player.money += round(self.player.wager / 2)
                print(f'Player surrendered, lost ${round(self.player.wager / 2)}.')
            case _:
                print('Error!')
        print()
        