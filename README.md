# Blackjack-analysis-simulation
An object oriented python environment to simulate blackjack play under different rules and setups. Also able to optimize its own strategy using a genetic algorithm and statistical analysis method.

## Auto_Play.py
This file will automatically play as many hands of blackjack as configured, with a random deck and according to whatever rules are in the Ideal_Graph.py. It will also graph how the money changes over time given the initial bet and furthermore will graph how the win rates change with the running count for counting purposes. I also implemented a counting method for changing the bet according to the running count to see how (ideally) card counting alters results. Below is an example graph found from 100,000 hands played by the accepted statistically optimal play strategy.
