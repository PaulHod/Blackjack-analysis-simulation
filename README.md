# Blackjack-analysis-simulation
An object oriented python environment to simulate blackjack play under different rules and setups. Also able to optimize its own strategy using a genetic algorithm and statistical analysis method.

## Auto_Play.py
This file will automatically play as many hands of blackjack as configured, with a random deck and according to whatever rules are in the Ideal_Graph.py. It will also graph how the money changes over time given the initial bet and furthermore will graph how the win rates change with the running count for counting purposes. I also implemented a counting method for changing the bet according to the running count to see how (ideally) card counting alters results. Below is an example graph found from 100,000 hands played by the accepted statistically optimal play strategy.

![Winnings vs Count](images/Winnings%20vs%20Count.png)
## Genetic_Algorithm
This folder contains the files necessary to run the genetic algorithm including main.py and genome.py. genome.py records the squares that make up the strategy chart and can chart them to display the results of the genetic algorithm and other strategy charts. Below is an example genome from a genetic algorithm experiment.

![Genetic Algorithm Chart](images/Genetic%20Algorithm.png)
As visible, it is fairly chaotic and not accurate to the official graph. This is because less common soft or pair hands are less common that the hard hands and thus did not factor into the scoring as much. This could be fixed by assuring each hand case was drawn evenly, yet the experiment did give me the idea for the statistical analysis method I later used.

## Statistical_Analysis
The files in this folder follow a more direct approach for analyzing blackjack strategy. Instead of random chances, each possible hand is dealt out, and a set number of hands are played with each combination of hand and dealer showing. After randomly performing each move a set number of hands, the move with the highest win chance is placed in its square in the strategy chart. This method was much faster than the genetic algorithm, and in much less time was able to generate a much more accurate chart seen below.

![Statistical Analysis Chart](images/Statistical_Analysis%20100000.png)
