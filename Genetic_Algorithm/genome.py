import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from Deck import Shoe
from Hand import Player_Hand, Dealer_Hand
from People import Person

class Genome:
    def __init__(self):
        self.Hard = np.zeros((10, 10))
        self.Soft = np.zeros((8, 10))
        self.Pairs = np.zeros((10, 10))

    def assign(self, hard, soft, pairs):
        self.Hard = hard.reshape(10,10)
        self.Soft = soft.reshape(8, 10)
        self.Pairs = pairs.reshape(10,10)

    def read(self, filename):
        with open(filename, "r") as f:
            self.data = json.load(f)

        self.Hard = np.array(self.data[0])
        self.Soft = np.array(self.data[1])
        self.Pairs = np.array(self.data[2])

    def write(self, filename):
        with open(filename, "w") as f:
            self.data = [self.Hard.tolist(), self.Soft.tolist(), self.Pairs.tolist()]
            json.dump(self.data, f)

    def linearize(self):
        return self.Hard.flatten(), self.Soft.flatten(), self.Pairs.flatten()

    def choose(self, showing, hand):
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
            option = self.Pairs[11-deck[hand.cards[0]]][deck[showing]-2]
        elif state == "hard":
            if total > 17: total = 17
            if total < 8: total = 8
            option = self.Hard[17-total][deck[showing]-2]
        elif state == "soft":
            if total > 20: total = 20
            if total < 13: total = 13
            option = self.Soft[20-total][deck[showing]-2]
        return option

    def analyze(self, hands, decks):
        self.counts = np.arange(-20,21,1/decks)
        self.wins_per_count = np.zeros_like(self.counts)
        self.occurences_per_count = np.zeros_like(self.counts)

        dealer = Person(0)
        player = Person(0)
        shoe = Shoe(decks)
        shoe.shuffle()
        for i in range(hands):
            dealer.deal(Dealer_Hand(shoe.draw(), shoe.draw()))
            showing = dealer.hands[0].showing()

            index = round((shoe.count/decks + 20) * decks)
            self.occurences_per_count[index] += 1

            player.deal(Player_Hand(shoe.draw(), shoe.draw(), 1))
            player.remove_money(1)
            for hand in player.hands:
                while not hand.standing:
            
                    move = self.choose(showing, hand)
                    if move == 1:
                        hand.hit(shoe.draw())
                    elif move == 0:
                        hand.stand()
                    elif move == 3:
                        player.hands.append(hand.split(shoe.draw(), shoe.draw()))
                        player.remove_money(1)
                    elif move == 2:
                        hand.double_down(shoe.draw())
                        player.remove_money(1)
        
                    if hand.total()[0] > 21:
                        continue

            # Dealer's turn
            while not dealer.hands[0].standing:
                dealer_total, dealer_move = dealer.hands[0].total()
                if dealer_move == "hit":
                    dealer.hands[0].hit(shoe.draw())
                elif dealer_move == "stand":
                    dealer.hands[0].stand()
            
            dealer_total = dealer.hands[0].total()[0]
            if dealer_total > 21:
                dealer_total = 0
            for hand in player.hands:
                count = hand.total()[0]
                if count > dealer_total and count <= 21: # Win Condition
                    if count == 21 and not hand.been_split and len(hand.cards) == 2:
                        winnings = hand.bet*1.5
                        self.wins_per_count[index] += winnings
                    else:
                        winnings = hand.bet
                        self.wins_per_count[index] += winnings
                    player.add_money(hand.bet+winnings)
                elif count == dealer_total:              # Push Condition
                    player.add_money(hand.bet)
                else:
                    self.wins_per_count[index] -= hand.bet

            player.reset()
            dealer.reset()
            shoe.reset()
            if i%(52*decks) == 0:
                shoe.shuffle()
        self.score = player.money/hands
        return self.score

    def display(self):
        strategy = np.vstack((self.Hard, self.Soft, self.Pairs))
        cmap = ListedColormap([
        "#e74c3c",  # red = stand
        "#2ecc71",  # green = hit
        "#3498db",  # blue = double
        "#f39c12"   # orange = split
        ])

        labels = ["S","H","D","P"]

        # Dealer's visible card
        dealer_cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "A"]

        # Player hands
        player_hands = [
            "17+", "16", "15", "14", "13", "12", "11", "10", "9", "8-","A,9","A,8","A,7","A,6","A,5","A,4","A,3","A,2","AA","TT","99","88","77","66","55","44","33","22"
        ]

        fig, ax = plt.subplots(figsize=(6, 8))

        ax.imshow(
            strategy,
            cmap=cmap,
            aspect="auto",
            vmin=-0.5,
            vmax=3.5
        )

        # Axis labels
        ax.set_xticks(np.arange(len(dealer_cards)))
        ax.set_xticklabels(dealer_cards)

        ax.set_yticks(np.arange(len(player_hands)))
        ax.set_yticklabels(player_hands)

        # Put dealer cards across the top
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position("top")

        ax.set_xlabel("Dealer's Up Card", fontsize=10, fontweight="bold")
        ax.set_ylabel("Your Hand", fontsize=10, fontweight="bold")

        # Write H/S/D/P into each square
        for row in range(strategy.shape[0]):
            for col in range(strategy.shape[1]):
                action = labels[strategy[row, col]]

                # White text on darker cells, black on light green/orange
                text_color = "white" if action in ["S", "D"] else "black"

                ax.text(
                    col,
                    row,
                    action,
                    ha="center",
                    va="center",
                    color=text_color,
                    fontsize=6
                )

        # White grid lines
        ax.set_xticks(np.arange(-0.5, strategy.shape[1], 1), minor=True)
        ax.set_yticks(np.arange(-0.5, strategy.shape[0], 1), minor=True)

        ax.grid(
            which="minor",
            color="white",
            linewidth=2
        )

        ax.tick_params(which="minor", bottom=False, left=False)

        # Title
        ax.set_title(
            "Blackjack Perfect Strategy (Dealer Stands Soft 17)",
            fontsize=12,
            fontweight="bold",
            pad=50
        )

        # Legend
        legend = [
            Patch(facecolor="#2ecc71", label="HIT"),
            Patch(facecolor="#e74c3c", label="STAND"),
            Patch(facecolor="#3498db", label="DOUBLE"),
            Patch(facecolor="#f39c12", label="SPLIT")
        ]

        ax.legend(
            handles=legend,
            loc="upper center",
            bbox_to_anchor=(0.5, -0.08),
            ncol=4,
            frameon=False
        )

        plt.tight_layout()
        plt.show()

gene = Genome()
gene.read("Statistical_Analysis/graph.json")
gene.display()