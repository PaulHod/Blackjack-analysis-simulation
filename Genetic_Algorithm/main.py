from Hand import Player_Hand, Dealer_Hand
from Deck import Shoe
from Player import Person

# Setup
decks = 1
num_players = 2
starting_cash = 100

# Initiation
dealer = Person(0)
players = []
for i in range(num_players):
    players.append(Person(starting_cash))
shoe = Shoe(decks)

# Game Loop
for i, player in enumerate(players):
    if player.money <= 0:
        print(f"Player {i+1}: Broke as hell")
    else:
        print(f"Player {i+1}: {player.get_money()}")
        # print(f"Hands: {player.hands}")

option = input("New hand? y/n: ").upper()
while option == "Y":
    for i, player in enumerate(players):
        print(f"Player {i+1}: {player.get_money()}, count is {shoe.count}")
        bet = int(input("Bet: $"))
        while bet > player.money:
            print("Bomboclatt u broke")
            bet = input("Bet: $")

        player.wager(bet)

    dealer.deal(Dealer_Hand(shoe.draw(), shoe.draw()))
    print(f"Dealer showing: {dealer.hands[0].showing()}")
    
    for i, player in enumerate(players):
            print(f"Player {i+1}: {player.get_money()}")
            player.deal(Player_Hand(shoe.draw(), shoe.draw(), player.bet))
            for j, hand in enumerate(player.hands):
                 while not hand.standing:
                    if hand.total()[1] == "bust":
                        print(f"Hand {j+1}: {hand.cards}, Bust")
                        continue
                    elif hand.total()[0] == 21:
                        hand.stand()
                        print(hand.cards,"BLACKJACK")
                        continue
                    print(f"Dealer showing: {dealer.hands[0].showing()}")
                    print(f"Hand {j+1}: {hand.cards}")
                    action = int(input("1.hit, 2.stand, 3.double, or 4.split: "))
                    if action == 1:
                        hand.hit(shoe.draw())
                    elif action == 2:
                        hand.stand()
                    elif action == 3:
                        if player.money < player.bet:
                            print("Inadequate Funds, hit or stand")
                            continue
                        player.remove_money(player.bet)
                        hand.double_down(shoe.draw())
                    elif action == 4:
                        if player.money < bet:
                            print("Inadequate Funds, hit or stand")
                            continue
                        player.remove_money(player.bet)
                        player.hands.append(hand.split(shoe.draw(), shoe.draw()))


    # Dealer's turn
    while not dealer.hands[0].standing:
        dealer_hand = dealer.hands[0].cards
        dealer_total, dealer_move = dealer.hands[0].total()
        print(f"Dealer's hand: {dealer_hand}, total = {dealer_total}")
        if dealer_move == "hit":
            print("Dealer Hits")
            dealer.hands[0].hit(shoe.draw())
        elif dealer_move == "stand":
            print("Dealer Stands")
            dealer.hands[0].stand()
        elif dealer_move == "bust":
            print("Dealer Busts")

    # Figure out winner
    if dealer_total > 21:
        dealer_total = 0
    for i, player in enumerate(players):
        for hand in player.hands:
                count = hand.total()[0]
                if count > dealer_total and count <= 21: # Win Condition
                    if count == 21 and not hand.been_split and len(hand.cards) == 2:
                        winnings = hand.bet*1.5
                    else:
                        winnings = hand.bet
                    player.add_money(hand.bet+winnings)
                    print(f"Player {i+1} wins ${winnings:.2f}")
                elif count == dealer_total:              # Push Condition
                    player.add_money(hand.bet)
                    print(f"Player {i+1} splits")
                else:
                    print(f"Player {i+1} looses ${hand.bet:.2f}")
        player.reset()

    dealer.reset()
    shoe.reset()
    
    option = input("New hand? y/n: ").upper()