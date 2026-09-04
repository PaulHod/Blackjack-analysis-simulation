class Hand:
    """Super class for other hand types, defines card values along with initiation with two cards, hit function, and stand function"""
    deck = {
        "A": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10
    }
    """Contains values corresponding to all cards"""

    # Initiates Hand with two cards
    def __init__(self, card1, card2):
        """Provide two cards, puts them in cards"""
        self.cards = [card1, card2]
        """The current cards in the hand"""
        self.standing = False
        """A flag to denote if hand has stood"""

    # Adds a new card to hand
    def hit(self, card):
        """Appends card to cards list"""
        self.cards.append(card.upper())

    # Changes the status to stand
    def stand(self):
        """Changes standing flag to true"""
        self.standing = True


class Dealer_Hand(Hand):
    """Subclass for dealer, has a showing function to denote which card is showing along with total function to calculate total
    and denote if dealer is standing or playing"""

    def __init__(self, card1, card2):
        super().__init__(card1, card2)
        """Provide two cards, puts them in cards"""
        self.cards = [card1, card2]
        self.original = card1
        """The current cards in the hand"""
        self.standing = False
        """A flag to denote if hand has stood"""

    def showing(self):
        """Returns dealer's showing card"""
        return self.cards[0]

    # Returns total and stands
    def total(self):
        """Calculates dealer value and weather they stand, bust, or keep playing"""
        sum = 0
        ace_counted = False
    
        # Calculate Hard Total
        for card in self.cards:
            sum += self.deck[card]
            if card == "A" and not ace_counted:
                sum += 10
                ace_counted = True
    
        state = "hit"
        if ace_counted == True and sum > 21:
            sum -= 10

        if sum >= 17 and sum <= 21:
            state = "stand"
            self.stand()
        elif sum > 21:
            state = "bust"
            self.stand()
    
        return sum, state

    def reset(self, card):
        self.cards = [self.original, card]
        self.standing = False

class Player_Hand(Hand):
    """Subclass for player's hand, can calculate total, split, and needs to be able to bet"""
    def __init__(self, card1, card2, bet):
        super().__init__(card1, card2)
        self.bet = bet
        self.original_bet = bet
        """How much money is at play"""
        self.original_cards = [card1, card2]
        self.been_split = False

    # Returns total and hard/soft
    def total(self):
        """Calculates total and returns number along with if it is hard, soft, or busts"""
        sum = 0
        ace_counted = False

        # Calculate Hard Total
        for card in self.cards:
            sum += self.deck[card]
            if card == "A" and not ace_counted:
                sum += 10
                ace_counted = True

        state = "hard"
        if ace_counted == True and sum > 21:
            sum -= 10
        elif ace_counted == True:
            state = "soft"

        if sum > 21:
            state = "bust"
            self.stand()

        return (sum, state)

    def double_down(self, card):
        """doubles the bet"""
        if len(self.cards) == 2 and not self.been_split:
            self.bet *= 2
            self.stand()
        self.hit(card)

    def split(self, card1, card2):
        """Draws two cards and implements split, returns new hand"""
        new_hand = Player_Hand(self.cards[1], card2, self.bet)
        self.cards[1] = card1
        self.been_split = True
        new_hand.been_split = True
        return new_hand

    def get_bet(self):
        return self.bet

    def reset(self):
        self.been_split = False
        self.bet = self.original_bet
        self.cards = self.original_cards.copy()
        self.standing = False
