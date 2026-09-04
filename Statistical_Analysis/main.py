import json
from Deck import Shoe
from Statistical_Analysis.Hand import Hand, Player_Hand, Dealer_Hand
import numpy as np
import random
import time
from timer import Timer

hands_per_square = 100000
shoe = Shoe(10)

hard_blank = np.zeros((10, 10), dtype=int)
soft_blank = np.zeros((8,10), dtype=int)

graph = [hard_blank.copy(),soft_blank.copy(),hard_blank.copy()]

occurences_double = [hard_blank.copy(),soft_blank.copy(),hard_blank.copy()]
occurences_hit  = [hard_blank.copy(),soft_blank.copy(),hard_blank.copy()]
occurences_split = [hard_blank.copy(),soft_blank.copy(),hard_blank.copy()]
occurences_stay = [hard_blank.copy(),soft_blank.copy(),hard_blank.copy()]
rewards_double  = [hard_blank.copy(),soft_blank.copy(),hard_blank.copy()]
rewards_hit     = [hard_blank.copy(),soft_blank.copy(),hard_blank.copy()]
rewards_split   = [hard_blank.copy(),soft_blank.copy(),hard_blank.copy()]
rewards_stay    = [hard_blank.copy(),soft_blank.copy(),hard_blank.copy()]

hard_blank = np.zeros((10, 10), dtype=float)
soft_blank = np.zeros((8,10), dtype=float)

stay_chances    = [hard_blank.copy(),soft_blank.copy(),hard_blank.copy()]
hit_chances     = [hard_blank.copy(),soft_blank.copy(),hard_blank.copy()]
double_chances  = [hard_blank.copy(),soft_blank.copy(),hard_blank.copy()]
split_chances   = [hard_blank.copy(),soft_blank.copy(),hard_blank.copy()]

timer = Timer(280)

with open("Statistical_Analysis/starting_hands.json", "r") as f:
    starting_hands = json.load(f)

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
        option = graph[2][11-deck[hand.cards[0]]][deck[showing]-2]
    elif state == "hard":
        if total > 17: total = 17
        if total < 8: total = 8
        option = graph[0][17-total][deck[showing]-2]
    elif state == "soft":
        if total > 20: total = 20
        if total < 13: total = 13
        option = graph[1][20-total][deck[showing]-2]
    return option

# Iterate Through all the squares
    # For each square iterate through all the hands
        # For each hand, play a random move followed by prescibed moves
        # Iterate scoring and occurences
    # Calculate win chances for each move
    # Assign said move to graph

dealer_starts = ["2","3","4","5","6","7","8","9","10","A"]
random.seed(time.time())

for k, segment in enumerate(graph):
# Setup each square
    for i, row in enumerate(segment):
        starting_hand = starting_hands[k][i]
        player = Player_Hand(starting_hand[0],starting_hand[1],1)
        print(player.total()[0])
        for j, bollocks in enumerate(row):
            dealer = Dealer_Hand(dealer_starts[j],shoe.draw())
            shoe.shuffle()
            showing = dealer.showing()
            print("Showing:",dealer.showing(), timer.update())
            for hand in range(hands_per_square):
                # Do first move
                if k == 2:
                    random_move = random.randint(0,3)
                else:
                    random_move = random.randint(0,2)

                if random_move == 0:
                    player.stand()
                elif random_move == 1:
                    player.hit(shoe.draw())
                elif random_move == 2:
                    player.double_down(shoe.draw())
                elif random_move == 3:
                    player.split(shoe.draw(),"2")
                player.total()
                # Player Now Plays the graph
                while not player.standing:
                    move = choose(showing, player)
                    if move == 0:
                        player.stand()
                    elif move == 1:
                        player.hit(shoe.draw())
                    elif move == 2:
                        player.double_down(shoe.draw())
                    player.total()
                # Dealer now plays
                while not dealer.standing:
                    dealer_total, dealer_move = dealer.total()
                    if dealer_move == "hit":
                        dealer.hit(shoe.draw())
                    elif dealer_move == "stand":
                        dealer.stand()
                    # elif dealer_move == "bust":
                    #     print("Dealer Busts")
                # Tally Points
                dealer_total, dealer_move = dealer.total()
                if dealer_total > 21:
                    dealer_total = 0
                count = player.total()[0]
                if count > dealer_total and count <= 21: # Win Condition
                    winnings = 1
                elif count == dealer_total:              # Push Condition
                    winnings = 0
                else:                                    # Loss Condition
                    winnings = -1
                # Iterate Arrays
                if random_move == 0:
                    rewards_stay[k][i][j] += winnings
                    occurences_stay[k][i][j] += 1
                elif random_move == 1:
                    rewards_hit[k][i][j] += winnings
                    occurences_hit[k][i][j] += 1
                elif random_move == 2:
                    rewards_double[k][i][j] += 2*winnings
                    occurences_double[k][i][j] += 1
                elif random_move == 3:
                    rewards_split[k][i][j] += 2*winnings
                    occurences_split[k][i][j] += 1
                # Reset hands
                player.reset()
                dealer.reset(shoe.draw())
                shoe.reset()
                if hand % 50 == 0:
                    shoe.shuffle()
            # Adjust Graph
            stay_win_chance = rewards_stay[k][i][j]/occurences_stay[k][i][j]
            hit_win_chance = rewards_hit[k][i][j]/occurences_hit[k][i][j]
            double_win_chance = rewards_double[k][i][j]/occurences_double[k][i][j]
            stay_chances[k][i][j] = stay_win_chance
            hit_chances[k][i][j] = hit_win_chance
            double_chances[k][i][j] = double_win_chance
            if k == 2:
                split_win_chance = rewards_split[k][i][j]/occurences_split[k][i][j]
                split_chances[k][i][j]= split_win_chance
            else:
                split_win_chance = -10
            options = [stay_win_chance, hit_win_chance, double_win_chance, split_win_chance]
            graph[k][i][j] = options.index(max(options))
        with open("Statistical_Analysis/graph.json", "w") as f:
            json.dump([graph[0].tolist(), graph[1].tolist(), graph[2].tolist()], f)
        with open("Statistical_Analysis/stay_chances.json", "w") as f:
            json.dump([stay_chances[0].tolist(), stay_chances[1].tolist(), stay_chances[2].tolist()], f)
        with open("Statistical_Analysis/hit_chances.json", "w") as f:
            json.dump([hit_chances[0].tolist(), hit_chances[1].tolist(), hit_chances[2].tolist()], f)
        with open("Statistical_Analysis/double_chances.json", "w") as f:
            json.dump([double_chances[0].tolist(), double_chances[1].tolist(), double_chances[2].tolist()], f)
        with open("Statistical_Analysis/split_chances.json", "w") as f:
            json.dump([hard_blank.copy().tolist(), soft_blank.copy().tolist(), split_chances[2].tolist()], f)
        