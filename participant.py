class Participant:
    def __init__(self, role):
        self.role = role
        self.new_round()
        
    def calculate_points(self):
        points = 0
        aces = []
        for card in self.hand:
            if card.rank != 'A':
                points += card.value
            else:
                aces.append(card)
        if aces:
            points += len(aces) * min(aces[0].value)
            if points + max(aces[0].value) - min(aces[0].value) <= 21:
                points += max(aces[0].value) - min(aces[0].value)
        self.points = points

    def new_round(self):
        self.hand = []
        self.points = 0


class Dealer(Participant):
    def __init__(self, role='dealer'):
        super().__init__(role)


class Player(Participant):
    def __init__(self, money, role='player'):
        super().__init__(role)
        self.money = money

    def bet(self, wager):
        self.money -= wager
        self.wager = wager

    def double_down(self):
        if self.money - self.wager >= 0:
            self.money -= self.wager
            self.wager *= 2
            return True
        return False


        