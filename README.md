# Blackjack Analysis & Simulation

An object-oriented Python environment for simulating blackjack under different rules and configurations. The project includes tools for simulating large numbers of hands, analyzing the effect of card counting, and automatically developing blackjack strategies using both genetic algorithms and statistical analysis.

## Auto_Play.py

`Auto_Play.py` simulates a configurable number of blackjack hands using the strategy defined in `Ideal_Graph.py`. The simulation tracks the player's bankroll over time and records win rates at different running counts to analyze the effect of card counting.

I also implemented a variable betting system that adjusts the bet according to the running count, allowing the simulation to compare how card counting and bet sizing affect long-term results.

Below is an example of the relationship between running count and winnings from a simulation of 100,000 hands using the accepted statistically optimal playing strategy.

![Winnings vs Count](images/Winnings%20vs%20Count.png)

## Genetic Algorithm

The `Genetic_Algorithm` folder contains the tools used to evolve blackjack strategies, primarily `main.py` and `genome.py`. Each genome represents a complete blackjack strategy chart, with individual decisions encoded for different combinations of player hands and dealer upcards. `genome.py` also contains tools for visualizing these strategies as conventional blackjack strategy charts.

Below is an example strategy produced during a genetic algorithm experiment.

![Genetic Algorithm Chart](images/Genetic%20Algorithm.png)

The resulting strategy is noticeably more chaotic than an established optimal strategy. One major limitation was the unequal frequency of different blackjack situations during random simulation. Hard hands occur much more frequently than many soft hands and pairs, causing performance on common hands to have a much greater influence on a genome's fitness.

Although the genetic algorithm did not consistently converge to the expected strategy, identifying this sampling problem led to the development of the more direct statistical analysis method used in the next part of the project.

## Statistical Analysis

The `Statistical_Analysis` folder uses a more controlled approach to generating a blackjack strategy. Rather than relying on the natural frequency of hands encountered during random play, the program explicitly evaluates each possible player-hand and dealer-upcard combination.

For each situation, each valid action is tested over a configurable number of simulated hands. The resulting performance of hitting, standing, doubling, or splitting is recorded, and the action with the highest estimated return is selected for that position in the strategy chart.

This approach ensures that uncommon situations receive meaningful sampling rather than being overshadowed by more frequently occurring hands. It also proved substantially faster at producing a strategy resembling established blackjack strategy than the genetic algorithm approach.

Below is an example strategy generated using the statistical analysis method.

![Statistical Analysis Chart](images/Statistical_Analysis%20100000.png)
