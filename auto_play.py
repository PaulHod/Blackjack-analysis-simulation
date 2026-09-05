import matplotlib.pyplot as plt
import numpy as np
import json

from Player import Person
from Hand import Player_Hand, Dealer_Hand
from Deck import Shoe
from Ideal_Play import choose
from timer import Timer

decks = 5
hands = 10000
bet   = 10

timer = Timer(hands)

dealer = Person(0)
player = Person(0)
shoe = Shoe(decks)

money = np.empty(dtype=int, shape=hands)
counts = np.arange(-20,21,1/decks)
wins_per_count = np.zeros_like(counts)
occurences_per_count = np.zeros_like(counts)

for i in range(hands):
    print(timer.update())
    money[i] = player.money
    index = round((shoe.true_count() + 20) * decks)
    occurences_per_count[index] += 1

    dealer.deal(Dealer_Hand(shoe.draw(), shoe.draw()))
    showing = dealer.hands[0].showing()

    # Counting Play
    if shoe.true_count() > 0:
        bet_modifier = 1 * shoe.true_count()
        player.deal(Player_Hand(shoe.draw(), shoe.draw(), bet_modifier*bet))
        player.remove_money(bet_modifier*bet)
    else:
        player.deal(Player_Hand(shoe.draw(), shoe.draw(), bet))
        player.remove_money(bet)

    # Regular Play
    # player.deal(Player_Hand(shoe.draw(), shoe.draw(), bet))
    # player.remove_money(bet)

    for hand in player.hands:
        while not hand.standing:

            move = choose(showing, hand).upper()
            if move == "HIT":
                hand.hit(shoe.draw())
            elif move == "STAND":
                hand.stand()
            elif move == "SPLIT":
                player.hands.append(hand.split(shoe.draw(), shoe.draw()))
                player.remove_money(bet)
            elif move == "DOUBLE":
                hand.double_down(shoe.draw())
                player.remove_money(bet)

            if hand.total()[0] > 21:
                continue

    # Dealer's turn
    while not dealer.hands[0].standing:
        dealer_hand = dealer.hands[0].cards
        dealer_total, dealer_move = dealer.hands[0].total()
        if dealer_move == "hit":
            dealer.hands[0].hit(shoe.draw())
        elif dealer_move == "stand":
            dealer.hands[0].stand()
        # elif dealer_move == "bust":
             # print("Dealer Busts")
    dealer_total = dealer.hands[0].total()[0]
    if dealer_total > 21:
        dealer_total = 0
    for hand in player.hands:
        count = hand.total()[0]
        if count > dealer_total and count <= 21: # Win Condition
            if count == 21 and not hand.been_split and len(hand.cards) == 2:
                winnings = hand.bet*1.5
                wins_per_count[index] += winnings/bet
            else:
                winnings = hand.bet
                wins_per_count[index] += winnings/bet
            player.add_money(hand.bet+winnings)
            # print(hand.cards, dealer_total, "WIN")
        elif count == dealer_total:              # Push Condition
            player.add_money(hand.bet)
            # print(hand.cards, dealer_total, "SPLIT")
        else:
            wins_per_count[index] -= hand.bet/bet
        #     print(hand.cards, dealer_total,"LOSS")
    player.reset()
    dealer.reset()
    if len(shoe.cards) < 25:
        shoe.reset()
        shoe.shuffle()

plt.plot(money)
plt.ylabel("Net Gain $")
plt.xlabel("Hands")
plt.title(f"Average % Change Per Hand: {100*money[-1]/(hands*bet):.2f}%")
plt.grid("both")
plt.show()

for i, win in enumerate(wins_per_count):
    if occurences_per_count[i] != 0:
        wins_per_count[i] = win/occurences_per_count[i]

# min_occurrences = 100
# valid_100 = occurences_per_count >= min_occurrences
min_occurrences = 1000
valid_1000 = occurences_per_count >= min_occurrences

# occurences_per_count = occurences_per_count/occurences_per_count.sum()
# wins_per_count = wins_per_count*occurences_per_count
# plt.plot(counts, occurences_per_count)
# plt.plot(counts, wins_per_count, label = "all")
# plt.plot(counts[valid_100], wins_per_count[valid_100], label="min occurences = 100")
plt.plot(counts[valid_1000], wins_per_count[valid_1000], label="min occurences = 1000")
# plt.legend()
plt.title("Winnings vs True Count")
plt.xlabel("True Count")
plt.ylabel("Average Return per Hand")
plt.grid("major")
plt.show()

with open(f"wins_occurences.json", "w") as f:
    json.dump([wins_per_count.tolist(),occurences_per_count.tolist()], f)