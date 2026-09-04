from Hand import Hand

class Person:
    def __init__(self, money):
        self.money = money
        self.hands = []
        self.bet = 0
        return
    
    def deal(self, hand):
        self.hands.append(hand)

    def reset(self):
        self.hands.clear()
        self.bet = 0

    def add_money(self, money):
        self.money += money

    def remove_money(self, money):
        self.money -= money

    def wager(self, bet):
        self.bet += bet
        self.money -= bet

    def get_money(self):
        return f"${self.money:.2f}"