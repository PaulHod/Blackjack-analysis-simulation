from Ideal_Graph import Hard, Soft, Pairs

def choose(showing, hand):
    deck = {
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
        "K": 10,
        "A": 11
    }

    total, state = hand.total()
    if hand.cards[0] == hand.cards[1]:
        option = Pairs[11-deck[hand.cards[0]]][deck[showing]-2]
    elif state == "hard":
        if total > 17: total = 17
        if total < 8: total = 8
        option = Hard[17-total][deck[showing]-2]
    elif state == "soft":
        if total > 20: total = 20
        if total < 13: total = 13
        option = Soft[20-total][deck[showing]-2]
    return option